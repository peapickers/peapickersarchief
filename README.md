# Peapickers Archive

Het archief van Peapickers: kunstpraktijken van mensen die maken buiten de kunstindustrie, veilig bewaard, beschreven en online getoond. **Het archief verkoopt niets.**

Gebouwd met [CollectionBuilder-CSV](https://collectionbuilder.github.io/) in dezelfde stijl als Peapicker's Postershop (Courier Prime, zwarte kaders van 1 px), maar met de eggshell-achtergrond van het archief (#F0EAD6) en zonder mand, prijzen of register.

Publiek adres (GitHub Pages): https://peapickers.github.io/peapickersarchive/

## Stand van zaken

Voorbeeldarchief: 10 fictieve archiefvormers (Voorbeeldmaker A tot J) met samen 127 fictieve archiefstukken (3 tot 30 per maker). Alle beelden zijn placeholders met watermerk. Zoekmachines en AI-crawlers worden voorlopig geweerd (`noindex: true` in `_config.yml` en `robots.txt`).

## Waar staat wat

| Bestand | Wat |
|---|---|
| `_data/peapickers-archief.csv` | Eén rij per archiefstuk: alle beschrijvende metadata, toegang en rechten. |
| `_data/archiefvormers.csv` | Eén rij per maker: nummer, praktijk, overeenkomst, datum van bewaargeving, korte biografie. |
| `objects/small/`, `objects/thumbs/` | De beelden die online staan: max. 1200 px en 450 px, met watermerk. **Nooit originelen.** |
| `_hulpscripts/afgeleiden.py` | Maakt die beelden uit de originelen op de archiefschijf. |
| `pages/about.md` | Tekst "Over het archief" (werkwijze, veilig tonen, rechten, verwijderen). |
| `pages/archiefvormers.md` | Pagina met alle archiefvormers. |

## Codes

`ARCHIEFSTUK2026-003-07` = in **2026** in het archief gekomen, archiefvormer **003**, zevende stuk. Dezelfde codering als de postershop. Een code verandert nooit en wordt nooit hergebruikt.

## Toegang per archiefstuk (kolom `toegang`)

- `Openbaar, met watermerk`: beschrijving en verkleind beeld met watermerk online. `display_template` = `image`.
- `Enkel beschrijving`: beeld wordt bewaard maar niet getoond. `display_template` = `record`, `image_small` en `image_thumb` leeg.
- `Embargo op het beeld`: zoals hierboven, tot de datum in `opmerking`.

## Een archiefstuk toevoegen

1. Voeg een rij toe aan `_data/peapickers-archief.csv` (kopieer een bestaande rij en pas aan).
2. Zet het origineel in een map op de archiefschijf, met de objectid als bestandsnaam (bv. `archiefstuk2026-011-01.tif`).
3. Draai `python3 _hulpscripts/afgeleiden.py /pad/naar/die/map` (vraagt Python 3 met Pillow).
4. Commit en push naar `main`. GitHub bouwt en publiceert de site vanzelf.

## Lokaal bouwen

Ruby 3.3: `bundle install`, dan `bundle exec jekyll serve` en open http://localhost:4000.

Regels voor wie aan de code werkt (mens of AI): zie `AGENTS.md`.
