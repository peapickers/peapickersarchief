# Maakt de beelden die het archief online toont: verkleind (max. 1200 px) en met watermerk "©<maker>".
# De originele bestanden van de makers komen NOOIT in deze repository; ze blijven op de archiefschijf.
#
# Werkwijze in drie stappen. Glaze moet de LAATSTE bewerking zijn voor een beeld online gaat:
# verkleinen en watermerken gebeurt dus eerst, en na Glaze wordt het grote beeld niet meer bewerkt.
#
#   1. python3 _hulpscripts/afgeleiden.py voorbereiden /pad/naar/originelen /pad/naar/te-glazen
#      Maakt per archiefstuk een verkleind beeld (max. 1200 px) met watermerk, als PNG.
#      In de map met originelen staat per archiefstuk één bestand met de objectid als naam,
#      bv. archiefstuk2026-001-01.tif of archiefstuk2026-001-01.jpg.
#   2. Open Glaze (gratis, Windows of Mac: https://glaze.cs.uchicago.edu), kies alle beelden uit
#      /pad/naar/te-glazen, intensiteit "Medium" of hoger, en laat Glaze ze in /pad/naar/geglazed zetten.
#   3. python3 _hulpscripts/afgeleiden.py publiceren /pad/naar/geglazed
#      Zet de geglazede beelden in objects/small/ (zonder ze opnieuw te verkleinen) en maakt de
#      kleine overzichtsbeelden in objects/thumbs/.
#
# Archiefstukken met toegang "Enkel beschrijving" of een lopend embargo worden overgeslagen.
#
# Het watermerk is schuin, over het hele beeld, onregelmatig geplaatst (per archiefstuk andere
# spreiding, grootte en hoek) en met omlijnde letters, zodat het moeilijk weg te werken is.
import csv, glob, os, random, sys
from PIL import Image, ImageDraw, ImageFont

HIER = os.path.dirname(os.path.abspath(__file__))
CB = os.path.dirname(HIER)
FB = '/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf'
MAX = 1200  # langste zijde van het getoonde beeld


def lettertype(grootte):
    try:
        return ImageFont.truetype(FB, grootte)
    except OSError:
        return ImageFont.load_default(size=grootte)


def watermerk(im, tekst, seed):
    rnd = random.Random(seed)
    w, h = im.size
    schaal = max(w, h) / 1200
    laag = Image.new('RGBA', (w * 2, h * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(laag)
    y, rij = 0, 0
    while y < h * 2:
        f = lettertype(int(rnd.randint(34, 48) * schaal))
        x = -rnd.randint(0, 400) + (rij % 2) * 180
        while x < w * 2:
            alpha = rnd.randint(70, 105)
            d.text((x, y), tekst, font=f, fill=(255, 255, 255, alpha),
                   stroke_width=2, stroke_fill=(0, 0, 0, alpha))
            x += int(d.textlength(tekst, font=f)) + int(rnd.randint(60, 160) * schaal)
        y += int(rnd.randint(95, 135) * schaal); rij += 1
    laag = laag.rotate(rnd.uniform(24, 36), resample=Image.BICUBIC)
    laag = laag.crop((w // 2, h // 2, w // 2 + w, h // 2 + h))
    d2 = ImageDraw.Draw(laag)
    for i in range(-h, w, rnd.randint(55, 70)):
        d2.line([(i, 0), (i + h * 0.6, h)], fill=(255, 255, 255, 22), width=1)
    return Image.alpha_composite(im.convert('RGBA'), laag).convert('RGB')


def bewaar(im, oid):
    obj = os.path.join(CB, 'objects')
    for sub, suf, sz in (('small', '_sm', MAX), ('thumbs', '_th', 450)):
        os.makedirs(f'{obj}/{sub}', exist_ok=True)
        t = im.copy(); t.thumbnail((sz, sz)); t.save(f'{obj}/{sub}/{oid}{suf}.jpg', quality=80)


def toonbaar(r):
    return r.get('image_small', '').strip() != ''


def rijen():
    for r in csv.DictReader(open(os.path.join(CB, '_data/peapickers-archief.csv'), encoding='utf-8')):
        if toonbaar(r):
            yield r
        else:
            print('overgeslagen (geen publiek beeld):', r['identiteitscode'])


def zoek(map_, oid):
    kand = glob.glob(os.path.join(map_, oid + '.*'))
    if not kand:
        print('ONTBREEKT:', oid)
    return kand[0] if kand else None


def voorbereiden(bron, doel):
    os.makedirs(doel, exist_ok=True)
    for r in rijen():
        pad = zoek(bron, r['objectid'])
        if not pad: continue
        im = Image.open(pad).convert('RGB'); im.thumbnail((MAX, MAX))
        watermerk(im, f"©{r['creator']}", r['objectid']).save(os.path.join(doel, r['objectid'] + '.png'))
        print('klaar voor Glaze:', r['identiteitscode'])


def publiceren(geglazed):
    obj = os.path.join(CB, 'objects')
    for sub in ('small', 'thumbs'):
        os.makedirs(f'{obj}/{sub}', exist_ok=True)
    for r in rijen():
        oid = r['objectid']
        pad = zoek(geglazed, oid)
        if not pad: continue
        im = Image.open(pad).convert('RGB')
        # het geglazede beeld zelf niet meer verkleinen; enkel opslaan als JPEG van hoge kwaliteit
        im.save(f'{obj}/small/{oid}_sm.jpg', quality=95)
        t = im.copy(); t.thumbnail((450, 450)); t.save(f'{obj}/thumbs/{oid}_th.jpg', quality=90)
        print('online klaar:', r['identiteitscode'])


if __name__ == '__main__':
    stap = sys.argv[1] if len(sys.argv) > 1 else ''
    if stap == 'voorbereiden' and len(sys.argv) == 4:
        voorbereiden(sys.argv[2], sys.argv[3])
    elif stap == 'publiceren' and len(sys.argv) == 3:
        publiceren(sys.argv[2])
    else:
        sys.exit(__doc__ or 'Gebruik: afgeleiden.py voorbereiden ORIGINELEN TE-GLAZEN  |  afgeleiden.py publiceren GEGLAZED')
