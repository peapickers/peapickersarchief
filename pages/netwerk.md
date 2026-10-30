---
title: Netwerk
layout: page
permalink: /netwerk.html
---

## Netwerk

Zo is het archief gegroeid: vanaf de archivaris, de eerste node, via wie wie aanbracht, en via de collectieven, clubs en vzw's waar archiefvormers bij horen. Sleep, zoom en klik op een node om zijn directe verbindingen te zien.

{% include feature/alert.html text="Voorbeeld. Alle archiefvormers, groepen en verbindingen in dit netwerk zijn fictief." color="warning" %}

{%- comment -%} Nodes en verbindingen komen uit _data/archiefvormers.csv (doorverwezen_door, groepen) en _data/groepen.csv. {%- endcomment -%}
{%- assign archiefvormers = site.data.archiefvormers -%}
{%- assign groepen = site.data.groepen -%}
<script id="netwerk-data" type="application/json">
{
  "archiefvormers": [{% for av in archiefvormers %}{"id": {{ av.nummer | jsonify }}, "naam": {{ av.naam | jsonify }}, "praktijk": {{ av.praktijk | jsonify }}, "plaats": {{ av.plaats | jsonify }}, "door": {{ av.doorverwezen_door | default: "" | jsonify }}, "groepen": {{ av.groepen | default: "" | jsonify }}, "url": {{ '/archiefvormers.html#av' | append: av.nummer | relative_url | jsonify }}}{% unless forloop.last %},{% endunless %}{% endfor %}],
  "groepen": [{% for g in groepen %}{"id": {{ g.code | jsonify }}, "naam": {{ g.naam | jsonify }}, "soort": {{ g.soort | jsonify }}, "plaats": {{ g.plaats | jsonify }}, "website": {{ g.website | default: "" | jsonify }}}{% unless forloop.last %},{% endunless %}{% endfor %}]
}
</script>

<div class="nw">
    <aside class="nw-paneel pp-filters" aria-label="Weergave van het netwerk">
        <fieldset class="pp-facet">
            <legend>Verbindingen</legend>
            <div class="form-check"><input class="form-check-input" type="checkbox" id="nw-door" checked><label class="form-check-label" for="nw-door">Doorverwijzingen</label></div>
            <div class="form-check"><input class="form-check-input" type="checkbox" id="nw-lid" checked><label class="form-check-label" for="nw-lid">Lid van een groep</label></div>
        </fieldset>
        <fieldset class="pp-facet" id="nw-groepen">
            <legend>Groepen</legend>
        </fieldset>
        <fieldset class="pp-facet">
            <legend>Egonetwerk</legend>
            <label class="form-label small mb-1" for="nw-diepte">Diepte rond de gekozen node: <span id="nw-diepte-tekst">1 stap</span></label>
            <input type="range" class="form-range" id="nw-diepte" min="1" max="2" step="1" value="1">
            <button type="button" class="btn btn-sm btn-outline-dark mt-2" id="nw-alles">Toon het hele archief</button>
        </fieldset>
        <div class="nw-legende small" aria-label="Legende">
            <span><i class="nw-bol nw-archivaris"></i>Archivaris</span>
            <span><i class="nw-bol nw-archiefvormer"></i>Archiefvormer</span>
            <span><i class="nw-bol nw-collectief"></i>Collectief</span>
            <span><i class="nw-bol nw-club"></i>Club</span>
            <span><i class="nw-bol nw-vzw"></i>Vzw</span>
        </div>
        <div id="nw-info" class="nw-info small" role="status" aria-live="polite">Klik op een node.</div>
    </aside>
    <div class="nw-veld" id="nw-veld" aria-label="Netwerkgrafiek van het archief"></div>
</div>

<script src="{{ '/assets/lib/d3.v7.8.5.min.js' | relative_url }}"></script>
<script>
(function () {
    if (!window.d3) { document.getElementById('nw-veld').textContent = 'De netwerkgrafiek kon niet laden.'; return; }
    var data = JSON.parse(document.getElementById('netwerk-data').textContent);
    var lijst = function (s) { return String(s || '').split(';').map(function (x) { return x.trim(); }).filter(Boolean); };
    function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }

    // Nodes: de archivaris (vast beginpunt), de archiefvormers en de groepen
    var nodes = [{ id: 'Jonas', naam: 'Jonas', soort: 'archivaris', info: 'Archivaris van Peapickers Archief' }];
    data.archiefvormers.forEach(function (a) { nodes.push({ id: a.id, naam: a.naam, soort: 'archiefvormer', info: 'Archiefvormer ' + a.id + ' · ' + a.praktijk + ', ' + a.plaats, url: a.url }); });
    data.groepen.forEach(function (g) { nodes.push({ id: g.id, naam: g.naam, soort: g.soort, info: g.soort.charAt(0).toUpperCase() + g.soort.slice(1) + ', ' + g.plaats, url: g.website }); });
    var perId = {}; nodes.forEach(function (n) { perId[n.id] = n; });
    var links = [];
    data.archiefvormers.forEach(function (a) {
        lijst(a.door).forEach(function (d) { if (perId[d]) links.push({ source: d, target: a.id, soort: 'door' }); });
        lijst(a.groepen).forEach(function (g) { if (perId[g]) links.push({ source: a.id, target: g, soort: 'lid' }); });
    });
    var graad = {}; links.forEach(function (l) { graad[l.source] = (graad[l.source] || 0) + 1; graad[l.target] = (graad[l.target] || 0) + 1; });
    nodes.forEach(function (n) { n.r = 6 + 2.2 * Math.sqrt(graad[n.id] || 0) * 2; });

    // Groepfilters
    var groepVak = document.getElementById('nw-groepen');
    data.groepen.forEach(function (g) {
        groepVak.insertAdjacentHTML('beforeend', '<div class="form-check"><input class="form-check-input nw-groep" type="checkbox" id="nw-g-' + esc(g.id) + '" value="' + esc(g.id) + '" checked><label class="form-check-label" for="nw-g-' + esc(g.id) + '">' + esc(g.naam) + '</label></div>');
    });

    var veld = document.getElementById('nw-veld');
    var W = veld.clientWidth || 800, H = veld.clientHeight || 560;
    var svg = d3.select(veld).append('svg').attr('viewBox', [-W / 2, -H / 2, W, H]).attr('role', 'img').attr('aria-label', 'Netwerk van archivaris, archiefvormers en groepen');
    var wereld = svg.append('g');
    svg.call(d3.zoom().scaleExtent([0.3, 4]).on('zoom', function (e) { wereld.attr('transform', e.transform); }));

    var jonas = perId.Jonas; jonas.fx = 0; jonas.fy = 0;
    var sim = d3.forceSimulation(nodes)
        .force('link', d3.forceLink(links).id(function (d) { return d.id; }).distance(function (l) { return l.soort === 'lid' ? 100 : 130; }))
        .force('charge', d3.forceManyBody().strength(-520))
        .force('botsing', d3.forceCollide().radius(function (d) { return d.r + 10; }))
        .force('x', d3.forceX().strength(0.04)).force('y', d3.forceY().strength(0.04));

    var lijn = wereld.append('g').selectAll('line').data(links).join('line').attr('class', function (l) { return 'nw-lijn nw-lijn-' + l.soort; });
    var knoop = wereld.append('g').selectAll('g').data(nodes).join('g').attr('class', function (d) { return 'nw-knoop nw-' + d.soort; })
        .attr('tabindex', 0).attr('role', 'button').attr('aria-label', function (d) { return d.naam; });
    knoop.append('circle').attr('r', function (d) { return d.r; });
    knoop.append('text').attr('dy', function (d) { return d.r + 13; }).text(function (d) { return d.naam; });
    knoop.call(d3.drag()
        .on('start', function (e, d) { if (!e.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
        .on('drag', function (e, d) { d.fx = e.x; d.fy = e.y; })
        .on('end', function (e, d) { if (!e.active) sim.alphaTarget(0); if (d !== jonas) { d.fx = null; d.fy = null; } }));
    sim.on('tick', function () {
        lijn.attr('x1', function (l) { return l.source.x; }).attr('y1', function (l) { return l.source.y; }).attr('x2', function (l) { return l.target.x; }).attr('y2', function (l) { return l.target.y; });
        knoop.attr('transform', function (d) { return 'translate(' + d.x + ',' + d.y + ')'; });
    });

    // Zichtbaarheid: soorten verbindingen, groepen en het egonetwerk rond de gekozen node
    var gekozen = null, diepte = 1;
    function zichtbareLinks() {
        var door = document.getElementById('nw-door').checked, lid = document.getElementById('nw-lid').checked;
        var aan = {}; document.querySelectorAll('.nw-groep').forEach(function (c) { aan[c.value] = c.checked; });
        return links.filter(function (l) {
            if (l.soort === 'door' && !door) return false;
            if (l.soort === 'lid' && (!lid || !aan[l.target.id])) return false;
            return true;
        });
    }
    function buren(id, ls) { var b = {}; ls.forEach(function (l) { if (l.source.id === id) b[l.target.id] = 1; if (l.target.id === id) b[l.source.id] = 1; }); return b; }
    function teken() {
        var ls = zichtbareLinks(), zicht = {};
        var groepAan = {}; document.querySelectorAll('.nw-groep').forEach(function (c) { groepAan[c.value] = c.checked && document.getElementById('nw-lid').checked; });
        nodes.forEach(function (n) { zicht[n.id] = n.soort === 'archivaris' || n.soort === 'archiefvormer' || groepAan[n.id]; });
        if (gekozen) {
            var bereik = {}; bereik[gekozen.id] = 1; var rand = [gekozen.id];
            for (var i = 0; i < diepte; i++) {
                var nieuw = []; rand.forEach(function (id) { Object.keys(buren(id, ls)).forEach(function (b) { if (!bereik[b]) { bereik[b] = 1; nieuw.push(b); } }); }); rand = nieuw;
            }
            nodes.forEach(function (n) { zicht[n.id] = zicht[n.id] && !!bereik[n.id]; });
        }
        knoop.classed('nw-weg', function (d) { return !zicht[d.id]; }).classed('nw-gekozen', function (d) { return gekozen && d.id === gekozen.id; });
        lijn.classed('nw-weg', function (l) { return ls.indexOf(l) === -1 || !zicht[l.source.id] || !zicht[l.target.id]; });
    }
    function kies(d) {
        gekozen = d; teken();
        var info = '<strong>' + esc(d.naam) + '</strong><br>' + esc(d.info);
        if (d.url) info += '<br><a href="' + esc(d.url) + '">' + (d.soort === 'archiefvormer' ? 'Bekijk de archiefvormer' : 'Website') + '</a>';
        document.getElementById('nw-info').innerHTML = info;
    }
    knoop.on('click', function (e, d) { kies(d); })
        .on('keydown', function (e, d) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); kies(d); } })
        .on('mouseenter', function (e, d) {
            var b = buren(d.id, zichtbareLinks()); b[d.id] = 1;
            knoop.classed('nw-vaag', function (n) { return !b[n.id]; });
            lijn.classed('nw-vaag', function (l) { return l.source.id !== d.id && l.target.id !== d.id; });
        })
        .on('mouseleave', function () { knoop.classed('nw-vaag', false); lijn.classed('nw-vaag', false); });
    document.getElementById('nw-diepte').addEventListener('input', function (e) {
        diepte = +e.target.value; document.getElementById('nw-diepte-tekst').textContent = diepte === 1 ? '1 stap' : diepte + ' stappen'; teken();
    });
    document.getElementById('nw-alles').addEventListener('click', function () { gekozen = null; document.getElementById('nw-info').textContent = 'Klik op een node.'; teken(); });
    document.querySelectorAll('#nw-door, #nw-lid, .nw-groep').forEach(function (c) { c.addEventListener('change', teken); });
    teken();
})();
</script>
