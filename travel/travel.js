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

  // ---------- data ----------
  const trips = TRIPS.map((t, i) => ({
    ...t,
    id: t.id || slug(t.name),
    stops: t.stops || [],
    year: yearOf(t.when),
    order: i,
  }));
  const tripById = new Map(trips.map(t => [t.id, t]));

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
    const atlas = byAtlas.has(name) ? name : null;
    const p = { name, region: null, atlas };
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
  const gLand = g.append("g"), gRoutes = g.append("g"), gPins = g.append("g");
  let W, H, current = null; // current = {type:"trip"|"place", ...}

  function showTip(e, text) {
    const r = mapEl.getBoundingClientRect();
    tip.textContent = text; tip.style.left = (e.clientX - r.left) + "px"; tip.style.top = (e.clientY - r.top) + "px"; tip.style.opacity = 1;
  }
  function hideTip() { tip.style.opacity = 0; }

  function draw() {
    gLand.selectAll("path").data(countries, d => d.properties.name).join("path")
      .attr("class", d => "country" + (visitedAtlas.has(d.properties.name) ? " v" : ""))
      .attr("d", path)
      .on("pointermove", (e, d) => {
        const n = d.properties.name;
        if (visitedAtlas.has(n)) showTip(e, (placeByAtlas.get(n) || { name: n }).name); else hideTip();
      })
      .on("pointerleave", hideTip)
      .on("click", (e, d) => {
        const p = placeByAtlas.get(d.properties.name) || (d.properties.name === "United Kingdom" && placeByName.get("United Kingdom"));
        if (p) go("country=" + encodeURIComponent(p.name));
      });

    gPins.selectAll("circle").data(places.filter(p => p.pin), d => d.name).join("circle")
      .attr("class", "pin").attr("cx", d => projection(d.pin)[0]).attr("cy", d => projection(d.pin)[1])
      .on("pointermove", (e, d) => showTip(e, d.name)).on("pointerleave", hideTip)
      .on("click", (e, d) => go("country=" + encodeURIComponent(d.name)));

    gRoutes.selectAll("g.route").data(trips.filter(t => t.stops.length > 1), d => d.id).join("g")
      .attr("class", "route").each(function (t) {
        const s = d3.select(this);
        const legs = t.stops.slice(1).map((to, i) => ({ from: t.stops[i], to, by: mode(to), trip: t }));
        const legPath = d => path({ type: "LineString", coordinates: [[d.from.lon, d.from.lat], [d.to.lon, d.to.lat]] });
        s.selectAll("path.route-line").data(legs).join("path")
          .attr("class", d => "route-line " + d.by).attr("d", legPath);
        s.selectAll("path.route-hit").data(legs).join("path")
          .attr("class", "route-hit").attr("d", legPath)
          .on("pointermove", (e, d) => showTip(e, current && current.trip === t
            ? `${d.from.name} → ${d.to.name} (${d.to.via || MODE_WORD[d.by]})`
            : t.name))
          .on("pointerleave", hideTip)
          .on("click", () => { if (!(current && current.trip === t)) go(t.id); });
        const uniq = [...new Map(t.stops.map(p => [p.name, p])).values()];
        s.selectAll("circle").data(uniq).join("circle").attr("class", "route-stop")
          .attr("cx", d => projection([d.lon, d.lat])[0]).attr("cy", d => projection([d.lon, d.lat])[1])
          .on("pointermove", (e, d) => showTip(e, d.name)).on("pointerleave", hideTip);
        s.selectAll("text").data(uniq).join("text").attr("class", "route-label").text(d => d.name)
          .attr("x", d => projection([d.lon, d.lat])[0]).attr("y", d => projection([d.lon, d.lat])[1]);
      });
    scaleMarks(d3.zoomTransform(svg.node()).k);
    applyFocus();
  }
  function scaleMarks(k) {
    gPins.selectAll("circle").attr("r", 5 / k);
    gRoutes.selectAll("circle").attr("r", 4 / k);
    gRoutes.selectAll("text").attr("font-size", 12 / k).attr("dx", 7 / k).attr("dy", 4 / k)
      .attr("display", k >= 3 ? null : "none");
  }
  const zoom = d3.zoom().scaleExtent([1, 40]).on("zoom", e => { g.attr("transform", e.transform); scaleMarks(e.transform.k); });
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
    const pad = Math.max(6, (b[1][0] - b[0][0]) * 0.08);
    return [[b[0][0] - pad, b[0][1] - pad], [b[1][0] + pad, b[1][1] + pad]];
  }
  function zoomToPlaces(ps) {
    const fs = ps.map(p => p.atlas && byAtlas.get(p.atlas)).filter(Boolean);
    if (fs.length) zoomToBounds(path.bounds({ type: "FeatureCollection", features: fs }), 8);
    else resetZoom();
  }
  function zoomToTrip(t) {
    const near = t.stops.filter(s => !s.far);
    if (near.length) zoomToBounds(boundsOf(near), 20);
    else if (t.stops.length) zoomToBounds(boundsOf(t.stops), 20);
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
    svg.classed("focus", !!(t || p));
    gRoutes.selectAll("g.route").classed("on", d => d === t);
    gLand.selectAll("path").classed("hl", d => {
      const pl = placeByAtlas.get(d.properties.name);
      return !!pl && hlPlaces.has(pl);
    });
    gPins.selectAll("circle").classed("hl", d => hlPlaces.has(d));
    gRoutes.selectAll("circle").classed("hl", false);
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
    const icons = filledLinks(t.links).map(([, i]) => i).join(" ");
    if (icons) b.appendChild(el("span", "ic", icons));
    b.appendChild(el("span", "t", t.name));
    const bits = [t.when];
    if (t.places.length) bits.push(t.places.length === 1 ? t.places[0].name : `${t.places.length} countries`);
    if (!t.stops.length) bits.push("route to come");
    b.appendChild(el("span", "m", bits.filter(Boolean).join(" · ")));
    b.addEventListener("click", () => go(t.id));
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
    panel.replaceChildren();
    panel.appendChild(el("h2", null, "Trips"));
    panel.appendChild(el("p", "intro", "Pick a trip to follow its route, or tap a highlighted country on the map."));
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
    panel.replaceChildren(backButton());
    panel.appendChild(el("h2", null, t.name));
    if (t.when) panel.appendChild(el("p", "when", t.when));
    if (t.note) panel.appendChild(el("p", "note", t.note));
    const lr = linksRow(t.links); if (lr) panel.appendChild(lr);

    if (t.places.length) {
      panel.appendChild(el("h3", null, "Countries"));
      panel.appendChild(placeChips(t.places, p => go("country=" + encodeURIComponent(p.name))));
    }
    if (!t.stops.length) {
      panel.appendChild(el("p", "empty", "Route still to be remembered."));
      return;
    }
    panel.appendChild(el("h3", null, "Route"));
    // Group consecutive stops by `part` (legs).
    const groups = [];
    t.stops.forEach((s, i) => {
      const key = s.part || null;
      const last = groups[groups.length - 1];
      if (last && last.key === key) last.stops.push([s, i]); else groups.push({ key, stops: [[s, i]] });
    });
    let activeBtn = null;
    groups.forEach(gr => {
      if (gr.key) {
        const h = el("button", "leg-head");
        h.appendChild(el("span", null, gr.key));
        const info = t.partInfo && t.partInfo[gr.key];
        if (info) h.appendChild(el("small", null, info));
        h.addEventListener("click", () => zoomToBounds(boundsOf(t.stops.filter(s => s.part === gr.key)), 24));
        panel.appendChild(h);
      }
      const ul = el("ul", "stops");
      gr.stops.forEach(([s, i]) => {
        const li = el("li");
        const b = el("button", "stop");
        const by = el("span", "by", i ? MODE_ICON[mode(s)] : "●");
        if (!i) by.classList.add("dot");
        if (i) by.title = s.via || MODE_WORD[mode(s)];
        b.appendChild(by);
        b.appendChild(el("span", null, s.name));
        const icons = filledLinks(s.links).map(([, ic]) => ic).join(" ");
        if (icons) b.appendChild(el("span", "by", icons));
        b.addEventListener("click", () => {
          if (activeBtn) activeBtn.classList.remove("on");
          b.classList.add("on"); activeBtn = b;
          gRoutes.selectAll("g.route.on circle").classed("hl", d => d.name === s.name);
          zoomToPoint([s.lon, s.lat], 24);
          if (matchMedia("(max-width: 900px)").matches) mapEl.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "center" });
        });
        li.appendChild(b);
        const sl = linksRow(s.links, true); if (sl) li.appendChild(sl);
        ul.appendChild(li);
      });
      panel.appendChild(ul);
    });
  }

  function renderPlace(p) {
    panel.replaceChildren(backButton());
    panel.appendChild(el("h2", null, p.name));
    if (p.region) panel.appendChild(el("p", "when", p.region));
    const ts = tripsForPlace(p);
    panel.appendChild(el("h3", null, ts.length ? (ts.length === 1 ? "On this trip" : `On ${ts.length} trips`) : "Trips"));
    if (ts.length) ts.forEach(t => panel.appendChild(tripButton(t)));
    else panel.appendChild(el("p", "empty", "Been here. The trip details are still to come."));
  }

  // ---------- routing (URL hash) ----------
  function go(hash) {
    const target = hash ? "#" + hash : location.pathname + location.search;
    if (("#" + hash) === location.hash || (!hash && !location.hash)) route();
    else history.pushState(null, "", target), route();
  }
  function route() {
    const h = decodeURIComponent(location.hash.slice(1));
    hideTip();
    if (h.startsWith("country=")) {
      const p = placeByName.get(h.slice(8));
      if (p) { current = { place: p }; renderPlace(p); applyFocus(); zoomToPlace(p); return; }
    } else if (tripById.has(h)) {
      const t = tripById.get(h);
      current = { trip: t }; renderTrip(t); applyFocus(); zoomToTrip(t); return;
    }
    current = null; renderHome(); applyFocus(); resetZoom();
  }
  window.addEventListener("popstate", route);
  document.addEventListener("keydown", e => { if (e.key === "Escape" && current) go(""); });

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
    const k = d3.zoomTransform(svg.node()); size(); svg.call(zoom.transform, k);
  }).observe(mapEl);
})();
