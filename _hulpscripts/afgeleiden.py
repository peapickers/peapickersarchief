# Maakt de beelden die het archief online toont: verkleind (max. 1200 px) en met watermerk "©<maker>".
# De originele bestanden van de makers komen NOOIT in deze repository; ze blijven op de archiefschijf.
#
# Gebruik:  python3 _hulpscripts/afgeleiden.py /pad/naar/originelen
#   In die map staat per archiefstuk één bestand met de objectid als naam,
#   bv. archiefstuk2026-001-01.tif of archiefstuk2026-001-01.jpg.
#   Archiefstukken met toegang "Enkel beschrijving" of een lopend embargo worden overgeslagen.
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


if __name__ == '__main__':
    bron = sys.argv[1]
    for r in csv.DictReader(open(os.path.join(CB, '_data/peapickers-archief.csv'), encoding='utf-8')):
        oid = r['objectid']
        if not toonbaar(r):
            print('overgeslagen (geen publiek beeld):', r['identiteitscode']); continue
        kand = glob.glob(os.path.join(bron, oid + '.*'))
        if not kand:
            print('ONTBREEKT:', oid); continue
        im = Image.open(kand[0]); im.thumbnail((MAX, MAX))
        bewaar(watermerk(im, f"©{r['creator']}", oid), oid)
        print('klaar:', r['identiteitscode'])
