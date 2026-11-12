// Travel page: one map, one side panel. Data lives in travel/trips.js.
(async function () {
  const LINK_KINDS = [
    ["album", "📷", "Photos"],
    ["emails", "✉️", "Emails"],
    ["memories", "💭", "Memories"],
    ["story", "📖", "Story"],
  ];
  const MODE_ICON = { flight: "✈︎", train: "🚆", boat: "⛴", bus: "🚌" };
  const MODE_WORD = { flight: "flight", train: "train", boat: "boat", bus: "bus" };
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const DUR = reduceMotion ? 0 : 750;

  const slug = s => s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const yearOf = when => { const m = String(when || "").match(/\d{4}/); return m ? +m[0] : null; };
  const lastYearOf = when => { const m = String(when || "").match(/\d{4}/g); return m ? +m[m.length - 1] : null; };
  const mode = s => (s.by === "flight" || s.by === "train" || s.by === "boat") ? s.by : "bus";
  const el = (tag, cls, text) => { const e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; };
  const filledLinks = links => LINK_KINDS.filter(([k]) => links && links[k]);
  const wait = ms => new Promise(r => setTimeout(r, ms));

  // ---------- data ----------
  const trips = TRIPS.map((t, i) => ({
    ...t,
    id: t.id || slug(t.name),
    stops: t.stops || [],
    year: yearOf(t.when),
    order: i,
  }));
  const tripById = new Map(trips.map(t => [t.id, t]));

  // Photo albums (travel/photos.js). A stop's `photos` is a slug or a list of slugs.
  const ALB = typeof ALBUMS === "undefined" ? {} : ALBUMS;
  const ownAlbums = s => [].concat(s.photos || []).filter(k => ALB[k]);
  // The gallery for a place on a trip gathers the albums from every visit to it.
  const placeAlbums = (t, name) => [...new Set(t.stops.filter(s => s.name === name).flatMap(ownAlbums))];
  const photoCount = slugs => slugs.reduce((n, k) => n + ALB[k].photos.length, 0);
  // A trip can also carry its own albums (e.g. a sketch trip with no route).
  trips.forEach(t => { t.hasPhotos = ownAlbums(t).length > 0 || t.stops.some(s => ownAlbums(s).length); });
  // Number each trip's places in the order they were first reached (start/end points like home aren't numbered).
  trips.forEach(t => {
    t.num = new Map();
    t.stops.forEach(s => { if (!s.far && !t.num.has(s.name)) t.num.set(s.name, t.num.size + 1); });
    t.uniq = [...new Map(t.stops.map(s => [s.name, s])).values()];
  });

  const svg = d3.select("#svg"), mapEl = document.getElementById("map"), tip = document.getElementById("tip");
  const panel = document.getElementById("panel");

  const WORLD = await (await fetch("travel/world.json")).json();
  const countries = topojson.feature(WORLD, WORLD.objects.countries).features.filter(f => f.properties.name !== "Antarctica");
  const byAtlas = new Map(countries.map(f => [f.properties.name, f]));

  // Places: PLACES plus any sketch-trip countries not already listed.
  const places = PLACES.map(p => ({ ...p }));
  const placeByName = new Map(places.map(p => [p.name, p]));
  trips.forEach(t => (t.countries || []).forEach(name => {
    if (placeByName.has(name)) return;
    const p = { name, region: null, atlas: byAtlas.has(name) ? name : null };
    places.push(p); placeByName.set(name, p);
  }));
  const placeByAtlas = new Map(places.filter(p => p.atlas).map(p => [p.atlas, p]));
  const visitedAtlas = new Set(placeByAtlas.keys());
  visitedAtlas.add("United Kingdom"); // Northern Ireland sits inside the UK shape

  // Which visited places each trip passed through (by stop location, plus listed countries).
  const bounds = new Map(countries.map(f => [f, d3.geoBounds(f)]));
  function placeAt(lon, lat) {
    for (const f of countries) {
      if (!visitedAtlas.has(f.properties.name)) continue;
      const [[w, s], [e, n]] = bounds.get(f);
      if (w <= e && (lon < w || lon > e || lat < s || lat > n)) continue;
      if (d3.geoContains(f, [lon, lat])) return placeByAtlas.get(f.properties.name) || placeByName.get("United Kingdom");
    }
    return null;
  }
  trips.forEach(t => {
    const seen = new Map();
    t.stops.forEach(s => { if (!s.far) { const p = placeAt(s.lon, s.lat); if (p) seen.set(p.name, p); } });
    (t.countries || []).forEach(n => { const p = placeByName.get(n); if (p) seen.set(p.name, p); });
    t.places = [...seen.values()];
  });
  const tripsForPlace = p => trips.filter(t => t.places.includes(p));

  // ---------- map ----------
  const projection = d3.geoNaturalEarth1();
  const path = d3.geoPath(projection);

  const g = svg.append("g");
  const gBase = g.append("g"), gLand = g.append("g"), gPins = g.append("g"), gRoutes = g.append("g");
  let W, H, current = null; // current = {trip} | {place} | null
  let playToken = 0;

  function showTip(e, text) {
    const r = mapEl.getBoundingClientRect();
    tip.textContent = text; tip.style.left = (e.clientX - r.left) + "px"; tip.style.top = (e.clientY - r.top) + "px"; tip.style.opacity = 1;
  }
  function hideTip() { tip.style.opacity = 0; }

  // A leg is drawn along the great circle, split where it wraps around the map edge.
  function legGeom(a, b) {
    const A = [a.lon, a.lat], B = [b.lon, b.lat];
    const n = Math.max(2, Math.ceil(d3.geoDistance(A, B) * 180 / Math.PI / 1.5));
    const ip = d3.geoInterpolate(A, B);
    const pts = []; let prev = null, total = 0;
    for (let i = 0; i <= n; i++) {
      const [x, y] = projection(ip(i / n));
      const brk = !prev || Math.abs(x - prev[0]) > W * 0.4;
      const len = brk ? 0 : Math.hypot(x - prev[0], y - prev[1]);
      total += len; pts.push({ x, y, brk, len }); prev = [x, y];
    }
    return { pts, total };
  }
  function partialD(geo, t) {
    if (t <= 0) return "";
    const target = t * geo.total; let acc = 0, d = "", last = null;
    for (const p of geo.pts) {
      if (p.brk) { d += `M${p.x},${p.y}`; last = p; continue; }
      if (acc + p.len >= target) {
        const f = p.len ? (target - acc) / p.len : 1;
        d += `L${last.x + (p.x - last.x) * f},${last.y + (p.y - last.y) * f}`;
        return d;
      }
      acc += p.len; d += `L${p.x},${p.y}`; last = p;
    }
    return d;
  }

  function draw() {
    gBase.selectAll("path.sphere").data([{ type: "Sphere" }]).join("path").attr("class", "sphere").attr("d", path);
    gBase.selectAll("path.grat").data([d3.geoGraticule10()]).join("path").attr("class", "grat").attr("d", path);

    gLand.selectAll("path").data(countries, d => d.properties.name).join("path")
      .attr("class", d => "country" + (visitedAtlas.has(d.properties.name) ? " v" : ""))
      .attr("d", path)
      .on("pointermove", (e, d) => {
        const n = d.properties.name;
        if (visitedAtlas.has(n)) showTip(e, (placeByAtlas.get(n) || { name: n }).name); else hideTip();
      })
      .on("pointerleave", hideTip)
      .on("click", (e, d) => {
        const p = placeByAtlas.get(d.properties.name);
        if (p) go("country=" + encodeURIComponent(p.name));
      });

    gPins.selectAll("circle").data(places.filter(p => p.pin), d => d.name).join("circle")
      .attr("class", "pin").attr("cx", d => projection(d.pin)[0]).attr("cy", d => projection(d.pin)[1])
      .on("pointermove", (e, d) => showTip(e, d.name)).on("pointerleave", hideTip)
      .on("click", (e, d) => go("country=" + encodeURIComponent(d.name)));

    gRoutes.selectAll("g.route").data(trips.filter(t => t.stops.length > 1), d => d.id).join("g")
      .attr("class", "route").each(function (t) {
        const s = d3.select(this);
        const legs = t.stops.slice(1).map((to, i) => {
          const from = t.stops[i];
          return { from, to, by: mode(to), geo: legGeom(from, to) };
        });
        // Glow = a wide, faint stroke under each line (SVG blur filters break in Safari when zoomed).
        s.selectAll("path.route-glow").data(legs).join("path")
          .attr("class", d => "route-glow " + d.by).attr("d", d => partialD(d.geo, 1));
        s.selectAll("path.route-line").data(legs).join("path")
          .attr("class", d => "route-line " + d.by).attr("d", d => partialD(d.geo, 1));
        s.selectAll("path.route-hit").data(legs).join("path")
          .attr("class", "route-hit").attr("d", d => partialD(d.geo, 1))
          .on("pointermove", (e, d) => showTip(e, current && current.trip === t
            ? `${d.from.name} → ${d.to.name} (${d.to.via || MODE_WORD[d.by]})`
            : t.name))
          .on("pointerleave", hideTip)
          .on("click", () => { if (!(current && current.trip === t)) go(t.id); });
        s.selectAll("g.wstop").data(t.uniq, d => d.name).join(enter => {
          const e = enter.append("g").attr("class", "wstop seen");
          e.append("circle");
          e.append("text").attr("class", "num");
          e.append("text").attr("class", "route-label");
          return e;
        })
          .classed("far", d => !t.num.has(d.name))
          .classed("has-photos", d => placeAlbums(t, d.name).length > 0)
          .attr("transform", d => `translate(${projection([d.lon, d.lat])})`)
          .on("pointermove", (e, d) => {
            const n = current && current.trip === t ? photoCount(placeAlbums(t, d.name)) : 0;
            showTip(e, n ? `${d.name} · 📷 ${n} photos` : d.name);
          }).on("pointerleave", hideTip)
          .on("click", (e, d) => {
            if (!(current && current.trip === t)) return;
            const a = placeAlbums(t, d.name);
            if (a.length) { e.stopPropagation(); hideTip(); go(`${t.id}/photos/${a[0]}`); }
          })
          .each(function (d) {
            const n = t.num.get(d.name);
            d3.select(this).select(".num").text(n || "");
            d3.select(this).select(".route-label").text(d.name);
          });
      });
    scaleMarks(d3.zoomTransform(svg.node()).k);
    applyFocus();
    cullLabels();
  }

  function scaleMarks(k) {
    gPins.selectAll("circle").attr("r", 3 / k);
    gRoutes.selectAll("g.route").each(function (t) {
      const on = current && current.trip === t;
      d3.select(this).selectAll("g.wstop").each(function (d) {
        const badge = on && t.num.has(d.name);
        const s = d3.select(this);
        s.select("circle").attr("r", (badge ? 8 : on ? 3 : 1.8) / k);
        s.select(".num").attr("font-size", 9.5 / k).attr("dy", "0.36em");
        s.select(".route-label").attr("font-size", 12 / k).attr("dx", (badge ? 11 : 7) / k).attr("dy", 4 / k);
      });
    });
  }

  // Show as many stop names as fit without overlapping, in visit order.
  function cullLabels() {
    const t = current && current.trip;
    gRoutes.selectAll(".route-label").attr("display", "none");
    if (!t) return;
    const tf = d3.zoomTransform(svg.node());
    const sel = gRoutes.selectAll("g.route").filter(d => d === t).selectAll("g.wstop.seen");
    const items = sel.nodes().map(n => {
      const d = d3.select(n).datum();
      const [x, y] = projection([d.lon, d.lat]);
      return { n, d, sx: tf.applyX(x), sy: tf.applyY(y), badge: t.num.has(d.name) };
    });
    const taken = items.map(i => ({ x0: i.sx - 9, y0: i.sy - 9, x1: i.sx + 9, y1: i.sy + 9 }));
    const hit = (a, b) => a.x0 < b.x1 && a.x1 > b.x0 && a.y0 < b.y1 && a.y1 > b.y0;
    items.sort((a, b) => (t.num.get(a.d.name) || 999) - (t.num.get(b.d.name) || 999)).forEach(i => {
      const x0 = i.sx + (i.badge ? 11 : 7), w = i.d.name.length * 6.6 + 4;
      const r = { x0, y0: i.sy - 9, x1: x0 + w, y1: i.sy + 7 };
      if (r.x1 > W || r.y0 < 0 || r.y1 > H || i.sx < 0) return;
      if (taken.some((o, j) => items[j] !== i && hit(r, o))) return;
      taken.push(r);
      d3.select(i.n).select(".route-label").attr("display", null);
    });
  }

  const zoom = d3.zoom().scaleExtent([1, 60])
    .on("zoom", e => { g.attr("transform", e.transform); scaleMarks(e.transform.k); })
    .on("end", cullLabels);
  svg.call(zoom).on("dblclick.zoom", null);

  function zoomToBounds([[x0, y0], [x1, y1]], maxK = 12) {
    const k = Math.min(maxK, 0.8 / Math.max((x1 - x0) / W, (y1 - y0) / H));
    svg.transition().duration(DUR).call(zoom.transform,
      d3.zoomIdentity.translate(W / 2, H / 2).scale(k).translate(-(x0 + x1) / 2, -(y0 + y1) / 2));
  }
  function zoomToFeature(f) {
    let target = f;
    if (f.geometry.type === "MultiPolygon" && ["United States of America", "France", "Netherlands", "Norway", "Chile", "Portugal", "Spain", "Ecuador", "Denmark"].includes(f.properties.name)) {
      const polys = f.geometry.coordinates.map(c => ({ type: "Polygon", coordinates: c }));
      target = polys.reduce((a, b) => d3.geoArea(a) > d3.geoArea(b) ? a : b);
    }
    zoomToBounds(path.bounds(target));
  }
  function zoomToPoint(ll, maxK = 30) { const [x, y] = projection(ll); zoomToBounds([[x - 12, y - 8], [x + 12, y + 8]], maxK); }
  function boundsOf(stops) {
    const pts = stops.map(s => projection([s.lon, s.lat]));
    const b = [[d3.min(pts, p => p[0]), d3.min(pts, p => p[1])], [d3.max(pts, p => p[0]), d3.max(pts, p => p[1])]];
    const pad = Math.max(0.8, Math.max(b[1][0] - b[0][0], b[1][1] - b[0][1]) * 0.12);
    return [[b[0][0] - pad, b[0][1] - pad], [b[1][0] + pad, b[1][1] + pad]];
  }
  function zoomToPlaces(ps) {
    const fs = ps.map(p => p.atlas && byAtlas.get(p.atlas)).filter(Boolean);
    if (fs.length) zoomToBounds(path.bounds({ type: "FeatureCollection", features: fs }), 8);
    else resetZoom();
  }
  function zoomToTrip(t) {
    const near = t.stops.filter(s => !s.far);
    if (near.length) zoomToBounds(boundsOf(near), 40);
    else if (t.stops.length) zoomToBounds(boundsOf(t.stops), 40);
    else zoomToPlaces(t.places);
  }
  function zoomToPlace(p) {
    if (p.pin) zoomToPoint(p.pin);
    else if (p.atlas && byAtlas.get(p.atlas)) zoomToFeature(byAtlas.get(p.atlas));
  }
  function resetZoom() { svg.transition().duration(reduceMotion ? 0 : 600).call(zoom.transform, d3.zoomIdentity); }
  d3.select("#zin").on("click", () => svg.transition().duration(300).call(zoom.scaleBy, 1.6));
  d3.select("#zout").on("click", () => svg.transition().duration(300).call(zoom.scaleBy, 1 / 1.6));
  d3.select("#zreset").on("click", resetZoom);

  function applyFocus() {
    const t = current && current.trip, p = current && current.place;
    const hlPlaces = new Set(t ? t.places : p ? [p] : []);
    svg.classed("focus", !!t).classed("place", !!p);
    gRoutes.selectAll("g.route").classed("on", d => d === t);
    gRoutes.selectAll("g.route.on").raise();
    gLand.selectAll("path").classed("hl", d => {
      const pl = placeByAtlas.get(d.properties.name);
      return !!pl && hlPlaces.has(pl);
    });
    gPins.selectAll("circle").classed("hl", d => hlPlaces.has(d));
    gRoutes.selectAll("g.wstop").classed("hl", false);
    scaleMarks(d3.zoomTransform(svg.node()).k);
  }

  // ---------- route animation ----------
  let stopButtons = [];   // panel buttons, one per stop index
  function markNow(i) {
    stopButtons.forEach((b, j) => b && b.classList.toggle("now", j === i));
  }
  function showAll() {
    gRoutes.selectAll("path.route-line, path.route-glow").interrupt().attr("d", d => partialD(d.geo, 1));
    gRoutes.selectAll("g.wstop").classed("seen", true);
  }
  function stopAnimation() { playToken++; showAll(); markNow(-1); cullLabels(); }

  async function play(t) {
    const my = ++playToken;
    showAll();
    if (reduceMotion) { zoomToTrip(t); cullLabels(); return; }
    const route = gRoutes.selectAll("g.route").filter(d => d === t);
    const lines = route.selectAll("path.route-line");
    const glows = route.selectAll("path.route-glow");
    const legs = lines.data(), nodes = lines.nodes(), glowNodes = glows.nodes();
    const stopSel = route.selectAll("g.wstop");
    const reveal = name => stopSel.filter(d => d.name === name).classed("seen", true);
    lines.attr("d", d => partialD(d.geo, 0));
    glows.attr("d", d => partialD(d.geo, 0));
    stopSel.classed("seen", false);
    reveal(t.stops[0].name); markNow(0);

    const hasParts = t.stops.some(s => s.part);
    if (!hasParts) { zoomToTrip(t); await wait(DUR + 100); }
    let part;
    const per = Math.max(160, Math.min(650, 16000 / legs.length));
    for (let i = 0; i < legs.length; i++) {
      if (my !== playToken) return;
      const leg = legs[i];
      if (hasParts && leg.to.part && leg.to.part !== part) {
        part = leg.to.part;
        zoomToBounds(boundsOf(t.stops.filter(s => s.part === part)), 40);
        await wait(DUR + 150);
        if (my !== playToken) return;
      }
      const dur = leg.by === "flight" ? per * 1.6 : per;
      try {
        await d3.selectAll([nodes[i], glowNodes[i]]).transition().duration(dur).ease(d3.easeCubicInOut)
          .attrTween("d", d => tt => partialD(d.geo, tt)).end();
      } catch (e) { return; }
      if (my !== playToken) return;
      reveal(leg.to.name); markNow(i + 1); cullLabels();
    }
    if (hasParts) { await wait(500); if (my === playToken) zoomToTrip(t); }
    setTimeout(() => { if (my === playToken) markNow(-1); }, 1500);
  }

  // ---------- panel ----------
  function linksRow(links, small) {
    const ls = filledLinks(links);
    if (!ls.length) return null;
    const row = el("div", "links" + (small ? " small" : ""));
    ls.forEach(([k, icon, label]) => {
      const a = el("a"); a.href = links[k]; a.target = "_blank"; a.rel = "noopener";
      a.textContent = `${icon} ${label}`; row.appendChild(a);
    });
    return row;
  }
  function tripButton(t) {
    const b = el("button", "trip-item" + (t.stops.length ? "" : " sketch"));
    const icons = filledLinks(t.links).map(([, i]) => i).concat(t.hasPhotos ? ["📷"] : []);
    if (icons.length) b.appendChild(el("span", "ic", [...new Set(icons)].join(" ")));
    b.appendChild(el("span", "t", t.name));
    const bits = [t.when];
    if (t.places.length) bits.push(t.places.length === 1 ? t.places[0].name : `${t.places.length} countries`);
    if (!t.stops.length && !ownAlbums(t).length) bits.push("route to come");
    b.appendChild(el("span", "m", bits.filter(Boolean).join(" · ")));
    b.addEventListener("click", () => go(t.id));
    const peek = on => gRoutes.selectAll("g.route").filter(d => d === t).classed("peek", on);
    b.addEventListener("mouseenter", () => peek(true));
    b.addEventListener("mouseleave", () => peek(false));
    return b;
  }
  function backButton() {
    const b = el("button", "back", "← All trips");
    b.addEventListener("click", () => go(""));
    return b;
  }
  function placeChips(ps, onPick) {
    const c = el("div", "chips");
    [...ps].sort((a, b) => a.name.localeCompare(b.name)).forEach(p => {
      const b = el("button", "chip", p.name);
      b.addEventListener("click", () => onPick(p, b));
      c.appendChild(b);
    });
    return c;
  }

  function renderHome() {
    stopButtons = [];
    panel.replaceChildren();
    panel.appendChild(el("h2", null, "Trips"));
    panel.appendChild(el("p", "intro", "Pick a trip to watch the route unfold, or tap a lit-up country on the map."));
    const sorted = [...trips].sort((a, b) => (b.year ?? -1) - (a.year ?? -1) || b.order - a.order);
    let lastYear;
    sorted.forEach(t => {
      if (t.year !== lastYear) { panel.appendChild(el("div", "year", t.year ?? "Undated")); lastYear = t.year; }
      panel.appendChild(tripButton(t));
    });
    if (!trips.length) panel.appendChild(el("p", "empty", "No trips yet."));
    panel.appendChild(el("h3", null, `All ${places.length} places`));
    panel.appendChild(placeChips(places, p => go("country=" + encodeURIComponent(p.name))));
  }

  function renderTrip(t) {
    stopButtons = [];
    panel.replaceChildren(backButton());
    panel.appendChild(el("h2", null, t.name));
    if (t.when) panel.appendChild(el("p", "when", t.when));
    if (t.note) panel.appendChild(el("p", "note", t.note));
    const lr = linksRow(t.links); if (lr) panel.appendChild(lr);

    if (t.places.length) {
      panel.appendChild(el("h3", null, "Countries"));
      panel.appendChild(placeChips(t.places, p => go("country=" + encodeURIComponent(p.name))));
    }
    if (ownAlbums(t).length) {
      panel.appendChild(el("h3", null, "Photos"));
      const pills = el("div", "album-pills");
      ownAlbums(t).forEach(k => {
        const b = el("button", "photos-btn", `📷 ${ALB[k].title} · ${ALB[k].photos.length}`);
        b.addEventListener("click", () => go(`${t.id}/photos/${k}`));
        pills.appendChild(b);
      });
      panel.appendChild(pills);
    }
    if (!t.stops.length) {
      if (!ownAlbums(t).length) panel.appendChild(el("p", "empty", "Route still to be remembered."));
      return;
    }
    const rh = el("div", "route-head");
    rh.appendChild(el("h3", null, "Route"));
    const replay = el("button", "replay", reduceMotion ? "Show whole route" : "▶ Replay");
    replay.addEventListener("click", () => play(t));
    rh.appendChild(replay);
    panel.appendChild(rh);

    // Group consecutive stops by `part` (legs).
    const groups = [];
    t.stops.forEach((s, i) => {
      const key = s.part || null;
      const last = groups[groups.length - 1];
      if (last && last.key === key) last.stops.push([s, i]); else groups.push({ key, stops: [[s, i]] });
    });
    groups.forEach(gr => {
      if (gr.key) {
        const h = el("button", "leg-head");
        h.appendChild(el("span", null, gr.key));
        const info = t.partInfo && t.partInfo[gr.key];
        if (info) h.appendChild(el("small", null, info));
        h.addEventListener("click", () => { stopAnimation(); zoomToBounds(boundsOf(t.stops.filter(s => s.part === gr.key)), 40); });
        panel.appendChild(h);
      }
      const ul = el("ul", "stops");
      gr.stops.forEach(([s, i]) => {
        const li = el("li");
        const b = el("button", "stop");
        const by = el("span", "by", i ? MODE_ICON[mode(s)] : "");
        if (i) by.title = "by " + (s.via || MODE_WORD[mode(s)]);
        b.appendChild(by);
        const n = t.num.get(s.name);
        b.appendChild(el("span", n ? "n" : "n home", n || "⌂"));
        b.appendChild(el("span", "nm", s.name));
        const icons = filledLinks(s.links).map(([, ic]) => ic).join(" ");
        if (icons) b.appendChild(el("span", "by", icons));
        b.addEventListener("click", () => {
          stopAnimation();
          markNow(i);
          gRoutes.selectAll("g.route.on g.wstop").classed("hl", d => d.name === s.name);
          zoomToPoint([s.lon, s.lat], 24);
          if (matchMedia("(max-width: 900px)").matches) mapEl.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        });
        stopButtons[i] = b;
        const row = el("div", "stop-row");
        row.appendChild(b);
        if (ownAlbums(s).length) {
          const all = placeAlbums(t, s.name);
          const pb = el("button", "photos-btn", `📷 ${photoCount(all)}`);
          pb.setAttribute("aria-label", `Photos from ${s.name} (${photoCount(all)})`);
          pb.addEventListener("click", () => go(`${t.id}/photos/${ownAlbums(s)[0]}`));
          row.appendChild(pb);
        }
        li.appendChild(row);
        const sl = linksRow(s.links, true); if (sl) li.appendChild(sl);
        ul.appendChild(li);
      });
      panel.appendChild(ul);
    });
  }

  function renderPlace(p) {
    stopButtons = [];
    panel.replaceChildren(backButton());
    panel.appendChild(el("h2", null, p.name));
    if (p.region) panel.appendChild(el("p", "when", p.region));
    const ts = tripsForPlace(p);
    panel.appendChild(el("h3", null, ts.length ? (ts.length === 1 ? "On this trip" : `On ${ts.length} trips`) : "Trips"));
    if (ts.length) ts.forEach(t => panel.appendChild(tripButton(t)));
    else panel.appendChild(el("p", "empty", "Been here. The trip details are still to come."));
  }

  // ---------- photo gallery ----------
  // URL: #<trip>/photos/<album>[/<n>]. One gallery per place on a trip, one section per album.
  const dlg = el("dialog", "gallery");
  dlg.innerHTML = `
    <div class="g-head"><div><h2></h2><p class="when"></p></div>
      <button class="g-close" aria-label="Close photos">✕</button></div>
    <div class="g-body"></div>
    <div class="g-viewer" hidden>
      <div class="g-bar"><button class="g-back">← All photos</button><span class="g-count"></span>
        <button class="g-close" aria-label="Close photos">✕</button></div>
      <figure><img alt=""><figcaption><span class="g-cap"></span><span class="g-date"></span></figcaption></figure>
      <button class="g-prev" aria-label="Previous photo">‹</button>
      <button class="g-next" aria-label="Next photo">›</button>
    </div>`;
  dlg.setAttribute("aria-label", "Photos");
  document.querySelector("main.travel").appendChild(dlg);
  const $ = sel => dlg.querySelector(sel);
  const viewer = $(".g-viewer"), vImg = $(".g-viewer img");
  let gal = null; // {trip, name, flat:[{k, i, p}], idx}
  let justClosed = false;
  const fmtDate = iso => new Date(iso + "T12:00:00Z")
    .toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric", timeZone: "UTC" });
  const galHash = (k, n) => `#${gal.trip.id}/photos/${k}` + (n ? "/" + n : "");
  const setHash = h => history.replaceState(history.state, "", h);

  // key = the stop name, or TRIP_KEY for the trip's own albums.
  const TRIP_KEY = "\u0000trip";
  function buildGallery(t, key, slugs) {
    gal = { trip: t, key, flat: slugs.flatMap(k => ALB[k].photos.map((p, i) => ({ k, i, p }))), idx: -1 };
    $(".g-head h2").textContent = key === TRIP_KEY ? t.name : key;
    $(".g-head .when").textContent = key === TRIP_KEY ? (t.when || "") : t.name;
    const body = $(".g-body"); body.replaceChildren(); body.scrollTop = 0;
    slugs.forEach(k => {
      const a = ALB[k], sec = el("section"); sec.id = "album-" + k;
      const h = el("h3", null, a.title);
      h.appendChild(el("small", null, [a.dates, `${a.photos.length} photos`].filter(Boolean).join(" · ")));
      sec.appendChild(h);
      if (a.note) sec.appendChild(el("p", "note", a.note));
      const grid = el("div", "g-grid");
      a.photos.forEach((p, i) => {
        const b = el("button", "g-thumb");
        const img = el("img"); img.src = p.src; img.loading = "lazy"; img.decoding = "async";
        img.width = p.w; img.height = p.h; img.alt = p.caption || `${a.title}, photo ${i + 1}`;
        b.appendChild(img);
        b.addEventListener("click", () => showPhoto(gal.flat.findIndex(f => f.k === k && f.i === i)));
        grid.appendChild(b);
      });
      sec.appendChild(grid);
      body.appendChild(sec);
    });
  }
  function showPhoto(idx) {
    const n = gal.flat.length;
    gal.idx = (idx + n) % n;
    const { k, i, p } = gal.flat[gal.idx];
    vImg.src = p.src; vImg.width = p.w; vImg.height = p.h; vImg.alt = p.caption || `${ALB[k].title}, photo ${i + 1}`;
    $(".g-cap").textContent = p.caption || (gal.flat.filter(f => f.k === k).length < gal.flat.length ? ALB[k].title : "");
    $(".g-date").textContent = p.date ? fmtDate(p.date) : "";
    $(".g-count").textContent = `${gal.idx + 1} / ${n}`;
    viewer.hidden = false;
    [1, -1].forEach(d => { const f = gal.flat[(gal.idx + d + n) % n]; if (f) new Image().src = f.p.src; });
    setHash(galHash(k, i + 1));
  }
  function hideViewer() {
    if (viewer.hidden) return;
    viewer.hidden = true;
    const f = gal.flat[gal.idx];
    if (f) {
      setHash(galHash(f.k));
      const th = dlg.querySelectorAll(`#album-${f.k} .g-thumb`)[f.i];
      if (th) th.focus({ preventScroll: true }), th.scrollIntoView({ block: "nearest" });
    }
  }
  function openGallery(t, slug, n) {
    const stop = t.stops.find(s => ownAlbums(s).includes(slug));
    const key = stop ? stop.name : ownAlbums(t).includes(slug) ? TRIP_KEY : null;
    if (key === null) return false;
    if (!gal || gal.trip !== t || gal.key !== key)
      buildGallery(t, key, stop ? placeAlbums(t, stop.name) : ownAlbums(t));
    if (!dlg.open) dlg.showModal();
    const idx = n ? gal.flat.findIndex(f => f.k === slug && f.i === n - 1) : -1;
    if (idx >= 0) showPhoto(idx);
    else {
      viewer.hidden = true;
      const sec = dlg.querySelector("#album-" + slug);
      if (sec && sec.previousElementSibling) sec.scrollIntoView({ block: "start" });
    }
    return true;
  }
  dlg.querySelectorAll(".g-close").forEach(b => b.addEventListener("click", () => dlg.close()));
  $(".g-back").addEventListener("click", hideViewer);
  $(".g-prev").addEventListener("click", () => showPhoto(gal.idx - 1));
  $(".g-next").addEventListener("click", () => showPhoto(gal.idx + 1));
  dlg.addEventListener("click", e => { if (e.target === dlg) dlg.close(); }); // backdrop
  dlg.addEventListener("cancel", e => { if (!viewer.hidden) { e.preventDefault(); hideViewer(); } });
  dlg.addEventListener("keydown", e => {
    if (viewer.hidden) return;
    if (e.key === "ArrowLeft") { e.preventDefault(); showPhoto(gal.idx - 1); }
    if (e.key === "ArrowRight") { e.preventDefault(); showPhoto(gal.idx + 1); }
  });
  let swipeX = null;
  const fig = $(".g-viewer figure");
  fig.addEventListener("pointerdown", e => { swipeX = e.clientX; });
  fig.addEventListener("pointerup", e => {
    if (swipeX == null) return;
    const dx = e.clientX - swipeX; swipeX = null;
    if (Math.abs(dx) > 50) showPhoto(gal.idx + (dx < 0 ? 1 : -1));
  });
  // Closing returns to the trip: step back if we opened it, otherwise rewrite the URL.
  dlg.addEventListener("close", () => {
    if (!location.hash.includes("/photos/")) return;
    if (history.state && history.state.gallery) { justClosed = true; history.back(); }
    else setHash("#" + gal.trip.id);
  });

  // ---------- routing (URL hash) ----------
  function go(hash) {
    if (("#" + hash) === location.hash || (!hash && !location.hash)) return route();
    history.pushState(hash.includes("/photos/") ? { gallery: true } : null, "", hash ? "#" + hash : location.pathname + location.search);
    route();
  }
  function route() {
    const h = decodeURIComponent(location.hash.slice(1));
    hideTip();
    const [tripId, photoPart] = h.split("/photos/");
    if (photoPart !== undefined && tripById.has(tripId)) {
      const t = tripById.get(tripId);
      if (!(current && current.trip === t)) {
        stopAnimation(); current = { trip: t }; renderTrip(t); applyFocus(); zoomToTrip(t);
      }
      const [k, n] = photoPart.split("/");
      if (openGallery(t, k, parseInt(n, 10) || 0)) return;
    }
    const fromGallery = dlg.open || justClosed;
    justClosed = false;
    if (dlg.open) dlg.close();
    if (fromGallery && current && current.trip && current.trip.id === h) return; // back to the trip as it was
    stopAnimation();
    if (h.startsWith("country=")) {
      const p = placeByName.get(h.slice(8));
      if (p) { current = { place: p }; renderPlace(p); applyFocus(); zoomToPlace(p); return; }
    } else if (tripById.has(h)) {
      const t = tripById.get(h);
      current = { trip: t }; renderTrip(t); applyFocus();
      if (t.stops.length > 1) play(t); else zoomToTrip(t);
      return;
    }
    current = null; renderHome(); applyFocus(); resetZoom();
  }
  window.addEventListener("popstate", route);
  document.addEventListener("keydown", e => { if (e.key === "Escape" && current && !dlg.open) go(""); });

  // ---------- summary + start ----------
  const years = trips.flatMap(t => [t.year, lastYearOf(t.when)]).filter(Boolean);
  const routed = trips.filter(t => t.stops.length > 1).length;
  document.getElementById("summary").textContent = [
    `${places.length} countries and territories`,
    `${trips.length} trip${trips.length === 1 ? "" : "s"}` + (routed < trips.length ? ` (${routed} mapped)` : ""),
    years.length ? `${Math.min(...years)}–${Math.max(...years)}` : null,
  ].filter(Boolean).join(" · ");

  function size() {
    const r = mapEl.getBoundingClientRect(); W = r.width; H = r.height;
    svg.attr("viewBox", `0 0 ${W} ${H}`);
    projection.fitExtent([[8, 8], [W - 8, H - 8]], { type: "FeatureCollection", features: countries });
    draw();
  }
  size();
  route();
  new ResizeObserver(() => {
    const r = mapEl.getBoundingClientRect();
    if (Math.abs(r.width - W) < 1 && Math.abs(r.height - H) < 1) return;
    const k = d3.zoomTransform(svg.node()); playToken++; size(); svg.call(zoom.transform, k);
  }).observe(mapEl);
})();
