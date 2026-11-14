#!/usr/bin/env python3
"""Import Facebook photo albums into the Travel page.

Usage (from the repo root):
    python3 -I tools/import_fb_albums.py EXPORT [EXPORT ...]

Pass every export at once (oldest first); each run rebuilds travel/photos/ from
scratch, so an export left off the command line loses its albums.

Reads <export>/your_facebook_activity/posts/album/*.html, copies each travel
album's photos to travel/photos/<slug>/NN.<ext>, and writes travel/photos.js.
Upload IP addresses and Facebook tracking links are never copied.
Albums are referenced from travel/trips.js by slug: {name:"Prague", ..., photos:"prague"}.
"""
import datetime
import glob
import html
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "travel", "photos")
OUT_JS = os.path.join(REPO, "travel", "photos.js")
TRIPS_JS = os.path.join(REPO, "travel", "trips.js")

# Album folders (prefix of <Name>_<id>) that are not travel albums.
SKIP = ("Coverphotos", "Profilepictures", "Mobileuploads", "iOSPhotos", "Photos",
        "GemstonePhotosAlbum")

IP_RE = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")


def text(fragment):
    t = re.sub(r"<[^>]+>", "", fragment)
    t = html.unescape(t).strip()
    # @[100000…:2048:Name] mention tokens -> Name
    return re.sub(r"@\[\d+:\d+:([^\]]+)\]", r"\1", t)


def parse_date(s):
    try:
        return datetime.datetime.strptime(s.strip(), "%b %d, %Y %I:%M:%S %p").date()
    except ValueError:
        return None


def slugify(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def month_range(dates):
    if not dates:
        return ""
    a, b = min(dates), max(dates)
    fa, fb = a.strftime("%b %Y"), b.strftime("%b %Y")
    if fa == fb:
        return fa
    if a.year == b.year:
        return f"{a.strftime('%b')} to {fb}"
    return f"{fa} to {fb}"


def dimensions(paths):
    """{path: (w, h)} via macOS sips, batched."""
    dims = {}
    for i in range(0, len(paths), 200):
        chunk = paths[i:i + 200]
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", *chunk],
                             capture_output=True, text=True).stdout
        cur = None
        for line in out.splitlines():
            if not line.startswith(" "):
                cur = line.strip()
                dims[cur] = [0, 0]
            elif "pixelWidth" in line:
                dims[cur][0] = int(line.split(":")[1])
            elif "pixelHeight" in line:
                dims[cur][1] = int(line.split(":")[1])
    return dims


def parse_album(path, export):
    t = open(path, encoding="utf-8").read()
    title = text(re.search(r"<h1[^>]*>(.*?)</h1>", t, re.S).group(1))
    m = re.search(r'<p class="_a70f">(.*?)</p>', t, re.S)
    note = text(m.group(1)) if m else ""
    photos = []
    for sec in re.findall(r'<section class="_a6-g">.*?</section>', t, re.S):
        src = re.search(r'<img src="([^"]+)"', sec)
        if not src:
            continue
        src = os.path.join(export, html.unescape(src.group(1)))
        cap = re.search(r'<div class="_3-95">(.*?)</div>', sec, re.S)
        cap = text(cap.group(1)) if cap else ""
        if cap == note:
            cap = ""
        taken = re.search(r'>Taken</div><div><div class="_a6-q">([^<]+)<', sec)
        upload = re.search(r'<div class="_a72d">([^<]+)<', sec)
        d = parse_date(taken.group(1)) if taken else None
        d = d or (parse_date(upload.group(1)) if upload else None)
        photos.append({"file": src, "caption": cap, "date": d})
    # Facebook often copies the album description onto each photo instead of the
    # album header. A caption shared by most of the album is really its note.
    caps = [p["caption"] for p in photos if p["caption"]]
    if caps:
        top = max(set(caps), key=caps.count)
        if caps.count(top) >= max(2, len(photos) / 2):
            note = note or top
            for p in photos:
                if p["caption"] == top:
                    p["caption"] = ""
    folder = os.path.basename(os.path.dirname(photos[0]["file"])) if photos else ""
    return title, note, folder, photos


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pages = []
    for arg in sys.argv[1:]:
        export = os.path.abspath(os.path.expanduser(arg))
        found = sorted(glob.glob(os.path.join(export, "your_facebook_activity/posts/album/*.html")))
        if not found:
            sys.exit("No album pages found under " + export)
        pages += [(p, export) for p in found]

    albums = []
    for p, export in pages:
        title, note, folder, photos = parse_album(p, export)
        if not photos or folder.rsplit("_", 1)[0] in SKIP:
            continue
        photos = [ph for ph in photos if os.path.isfile(ph["file"])
                  and not ph["file"].lower().endswith(".mp4")]
        if photos:
            albums.append((title, note, photos))

    first = lambda a: min((p["date"] for p in a[2] if p["date"]), default=datetime.date.max)
    albums.sort(key=first)

    if os.path.isdir(OUT_DIR):
        shutil.rmtree(OUT_DIR)
    os.makedirs(OUT_DIR)

    dims = dimensions([ph["file"] for _, _, ps in albums for ph in ps])
    data, used = {}, set()
    for title, note, photos in albums:
        slug = base = slugify(title)
        n = 2
        while slug in used:
            slug, n = f"{base}-{n}", n + 1
        used.add(slug)
        os.makedirs(os.path.join(OUT_DIR, slug))
        out = []
        for i, ph in enumerate(sorted(photos, key=lambda p: (p["date"] or datetime.date.max)), 1):
            ext = os.path.splitext(ph["file"])[1].lower()
            rel = f"travel/photos/{slug}/{i:02d}{ext}"
            shutil.copyfile(ph["file"], os.path.join(REPO, rel))
            w, h = dims.get(ph["file"], (0, 0))
            item = {"src": rel, "w": w, "h": h}
            if ph["caption"]:
                item["caption"] = ph["caption"]
            if ph["date"]:
                item["date"] = ph["date"].isoformat()
            out.append(item)
        data[slug] = {"title": title, "note": note,
                      "dates": month_range([p["date"] for p in photos if p["date"]]),
                      "photos": out}

    body = ",\n".join(f" {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in data.items())
    js = ("// GENERATED by tools/import_fb_albums.py from a Facebook export. Do not edit by hand;\n"
          "// re-run the script instead. Reference albums from trips.js by slug: photos:\"prague\".\n"
          "const ALBUMS = {\n" + body + "\n};\n")
    if IP_RE.search(js):
        sys.exit("Refusing to write photos.js: it contains an IP-address-like string.")
    open(OUT_JS, "w", encoding="utf-8").write(js)

    total = sum(len(v["photos"]) for v in data.values())
    print(f"{len(data)} albums, {total} photos -> travel/photos/, travel/photos.js\n")
    trips = open(TRIPS_JS, encoding="utf-8").read() if os.path.exists(TRIPS_JS) else ""
    refs = set(re.findall(r'"([a-z0-9-]+)"', " ".join(re.findall(r"photos:\s*(\[[^\]]*\]|\"[^\"]*\")", trips))))
    for slug, v in data.items():
        mark = " " if slug in refs else "*"
        print(f"{mark} {slug:45} {v['dates']:22} {len(v['photos']):3}")
    missing = refs - set(data)
    print("\n* = not referenced from trips.js yet")
    if missing:
        print("Referenced in trips.js but not found:", ", ".join(sorted(missing)))


if __name__ == "__main__":
    main()
