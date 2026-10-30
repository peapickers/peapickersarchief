---
title: Archiefvormers
layout: page
permalink: /archiefvormers.html
---

## Archiefvormers

Een archiefvormer is de auteur die zijn of haar werk in bewaring geeft. Elke archiefvormer krijgt een nummer: dat is het middelste deel van de code van elk archiefstuk (ARCHIEFSTUK2027-**003**-07 is het zevende stuk van archiefvormer 003).

{% include feature/alert.html text="Voorbeeld. Alle archiefvormers op deze pagina zijn fictief." color="warning" %}

{%- assign stukken = site.data[site.metadata] %}
<div class="av-lijst">
{% for av in site.data.archiefvormers %}
{%- assign eigen = stukken | where: "creator", av.naam -%}
{%- assign metbeeld = eigen | where_exp: "s", "s.image_thumb" -%}
<section class="av-kaart" id="av{{ av.nummer }}">
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
