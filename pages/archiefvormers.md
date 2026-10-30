---
title: Archiefvormers
layout: page
permalink: /archiefvormers.html
---

## Archiefvormers

Een archiefvormer is de auteur die zijn of haar werk in bewaring geeft. Elke archiefvormer krijgt een nummer: dat is het middelste deel van de code van elk archiefstuk (ARCHIEFSTUK2027-**003**-07 is het zevende stuk van archiefvormer 003).

{% include feature/alert.html text="Voorbeeld. Alle archiefvormers op deze pagina zijn fictief." color="warning" %}

{%- assign stukken = site.data[site.metadata] %}
<div class="pp-browse">
    <aside class="pp-filters" aria-label="Filters">
        <div class="d-flex justify-content-between align-items-baseline mb-2">
            <h2 class="h5 mb-0">Filters</h2>
            <button type="button" class="btn btn-link btn-sm p-0 text-dark" id="av-reset">Alles wissen</button>
        </div>
        <label class="visually-hidden" for="av-zoek">Zoeken</label>
        <input type="search" class="form-control mb-3" id="av-zoek" placeholder="Zoeken ...">
        <div id="av-facetten"></div>
    </aside>

    <section class="pp-resultaat" aria-label="Archiefvormers">
        <div class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-3">
            <div id="av-aantal" class="small" role="status" aria-live="polite"></div>
            <button type="button" class="btn btn-sm btn-outline-dark" id="av-shuffle" title="Alle filters wissen en de archiefvormers in willekeurige volgorde tonen">Shuffle</button>
        </div>
        <div class="av-lijst" id="av-lijst">
{% for av in site.data.archiefvormers %}
{%- assign eigen = stukken | where: "creator", av.naam -%}
{%- assign metbeeld = eigen | where_exp: "s", "s.image_thumb" -%}
{%- capture f_genre %}{% for s in eigen %}{{ s.genre }};{% endfor %}{% endcapture -%}
{%- capture f_techniek %}{% for s in eigen %}{{ s.techniek }};{% endfor %}{% endcapture -%}
{%- capture f_materiaal %}{% for s in eigen %}{{ s.materiaal }};{% endfor %}{% endcapture -%}
{%- capture f_subject %}{% for s in eigen %}{{ s.subject }};{% endfor %}{% endcapture -%}
{%- capture f_reeks %}{% for s in eigen %}{{ s.reeks }};{% endfor %}{% endcapture -%}
{%- capture f_toegang %}{% for s in eigen %}{{ s.toegang }};{% endfor %}{% endcapture -%}
<section class="av-kaart" id="av{{ av.nummer }}"
    data-praktijk="{{ av.praktijk | escape }}" data-plaats="{{ av.plaats | escape }}" data-bewaring="{{ av.datum | slice: 0, 4 }}"
    data-genre="{{ f_genre | escape }}" data-techniek="{{ f_techniek | escape }}" data-materiaal="{{ f_materiaal | escape }}"
    data-subject="{{ f_subject | escape }}" data-reeks="{{ f_reeks | escape }}" data-toegang="{{ f_toegang | escape }}">
    <p class="small mb-1">Archiefvormer {{ av.nummer }}</p>
    <h2>{{ av.naam }}</h2>
    <p class="mb-0">{{ av.praktijk | capitalize }}, {{ av.plaats }}</p>
    <dl>
        <dt>Periode</dt><dd>{{ av.periode }}</dd>
        <dt>In bewaring sinds</dt><dd>{{ av.datum }}</dd>
        <dt>Overeenkomst</dt><dd>Depotovereenkomst {{ av.overeenkomst }}</dd>
        <dt>Archiefstukken</dt><dd>{{ av.aantal }}, waarvan {{ av.getoond }} met beeld</dd>
    </dl>
    <p class="small">{{ av.bio }}</p>
    <div class="av-beelden" aria-hidden="true">
        {% for s in metbeeld limit: 4 %}<img src="{{ s.image_thumb | relative_url }}" alt="" loading="lazy">{% endfor %}
        {% if metbeeld.size == 0 %}<span class="av-leeg"></span><span class="small align-self-center">Geen beelden openbaar</span>{% endif %}
    </div>
    <p class="mt-3 mb-0"><a href="{{ '/index.html#creator:' | append: av.naam | relative_url }}">Bekijk de {{ av.aantal }} archiefstukken</a></p>
</section>
{% endfor %}
        </div>
        <p id="av-geen" hidden>Geen archiefvormers voor deze filters.</p>
    </section>
</div>

<script>
(function () {
    // Filters op de metadata van de archiefvormer en van al zijn of haar archiefstukken; waarden gescheiden door ";".
    var FACETTEN = [
        { veld: 'praktijk', naam: 'Praktijk' }, { veld: 'plaats', naam: 'Plaats' }, { veld: 'bewaring', naam: 'In bewaring sinds' },
        { veld: 'genre', naam: 'Genre' }, { veld: 'techniek', naam: 'Techniek' }, { veld: 'materiaal', naam: 'Materiaal' },
        { veld: 'subject', naam: 'Onderwerp' }, { veld: 'reeks', naam: 'Reeks' }, { veld: 'toegang', naam: 'Toegang' }
    ];
    var lijst = document.getElementById('av-lijst');
    var kaarten = Array.prototype.slice.call(lijst.querySelectorAll('.av-kaart'));
    var zoek = document.getElementById('av-zoek'), facDiv = document.getElementById('av-facetten');
    var gekozen = {};
    function waarden(k, veld) {
        var u = {}; String(k.dataset[veld] || '').split(';').forEach(function (w) { w = w.trim(); if (w) u[w] = true; });
        return Object.keys(u);
    }
    function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
    FACETTEN.forEach(function (f) {
        gekozen[f.veld] = new Set();
        var alle = {}; kaarten.forEach(function (k) { waarden(k, f.veld).forEach(function (w) { alle[w] = true; }); });
        var ws = Object.keys(alle).sort(function (a, b) { return a.localeCompare(b, 'nl', { numeric: true }); });
        if (!ws.length) return;
        var html = '<fieldset class="pp-facet"><legend>' + f.naam + '</legend>';
        ws.forEach(function (w, i) {
            var id = 'av-' + f.veld + '-' + i;
            html += '<div class="form-check"><input class="form-check-input" type="checkbox" id="' + id + '" data-veld="' + f.veld + '" value="' + esc(w) + '">' +
                '<label class="form-check-label d-flex justify-content-between gap-2" for="' + id + '"><span>' + esc(w) + '</span><span class="pp-telling" data-veld="' + f.veld + '" data-waarde="' + esc(w) + '"></span></label></div>';
        });
        facDiv.insertAdjacentHTML('beforeend', html + '</fieldset>');
    });
    function past(k, behalve) {
        var q = zoek.value.trim().toLowerCase();
        if (q && k.textContent.toLowerCase().indexOf(q) === -1) return false;
        return FACETTEN.every(function (f) {
            if (f.veld === behalve || !gekozen[f.veld].size) return true;
            return waarden(k, f.veld).some(function (w) { return gekozen[f.veld].has(w); });
        });
    }
    function teken() {
        var n = 0;
        kaarten.forEach(function (k) { var ok = past(k); k.hidden = !ok; if (ok) n++; });
        document.getElementById('av-aantal').textContent = n + (n === 1 ? ' archiefvormer' : ' archiefvormers');
        document.getElementById('av-geen').hidden = n > 0;
        facDiv.querySelectorAll('.pp-telling').forEach(function (el) {
            var veld = el.dataset.veld, w = el.dataset.waarde;
            var c = kaarten.filter(function (k) { return past(k, veld) && waarden(k, veld).indexOf(w) > -1; }).length;
            el.textContent = c; el.closest('.form-check').classList.toggle('pp-leeg', c === 0);
        });
    }
    function wis() {
        zoek.value = '';
        facDiv.querySelectorAll('input:checked').forEach(function (cb) { cb.checked = false; });
        FACETTEN.forEach(function (f) { gekozen[f.veld].clear(); });
    }
    facDiv.addEventListener('change', function (e) {
        var cb = e.target; if (!cb.dataset.veld) return;
        gekozen[cb.dataset.veld][cb.checked ? 'add' : 'delete'](cb.value); teken();
    });
    zoek.addEventListener('input', teken);
    document.getElementById('av-reset').addEventListener('click', function () { wis(); teken(); });
    // Shuffle: filters weg en de kaarten in een nieuwe willekeurige volgorde (Fisher-Yates).
    document.getElementById('av-shuffle').addEventListener('click', function () {
        wis();
        for (var i = kaarten.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = kaarten[i]; kaarten[i] = kaarten[j]; kaarten[j] = t; }
        kaarten.forEach(function (k) { lijst.appendChild(k); });
        teken();
    });
    teken();
})();
</script>
