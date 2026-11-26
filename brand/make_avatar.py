import math, numpy as np
from PIL import Image, ImageDraw
S = 2048
YEL, NAVY = (255, 210, 63), (9, 13, 28)
def glyph(d, cx, cy, arm, th, col):
    r = th / 2
    for ang in (90, 30, 150):
        a = math.radians(ang)
        dx, dy = math.cos(a) * arm, math.sin(a) * arm
        nx, ny = -math.sin(a) * r, math.cos(a) * r
        d.polygon([(cx - dx + nx, cy - dy + ny), (cx + dx + nx, cy + dy + ny),
                   (cx + dx - nx, cy + dy - ny), (cx - dx - nx, cy - dy - ny)], fill=col)
        for sx in (-1, 1):
            x, y = cx + sx * dx, cy + sx * dy
            d.ellipse([x - r, y - r, x + r, y + r], fill=col)
def navy_bg():
    yy = np.linspace(0, 1, S)[:, None]; xx = np.linspace(-1, 1, S)[None, :]
    top, bot = np.array([16, 23, 50.0]), np.array([5, 7, 15.0])
    bg = top[None, None, :] * (1 - yy)[..., None] + bot[None, None, :] * yy[..., None]
    bg = bg * (1 - 0.30 * (xx ** 2))[..., None]
    return Image.fromarray(np.clip(bg, 0, 255).astype(np.uint8))
en = navy_bg(); glyph(ImageDraw.Draw(en), S / 2, S / 2, 500, 236, YEL)
en.resize((1024, 1024), Image.LANCZOS).save("avatar_EN_with_an_asterisk.png")
es = Image.new("RGB", (S, S), YEL); glyph(ImageDraw.Draw(es), S / 2, S / 2, 500, 236, NAVY)
es.resize((1024, 1024), Image.LANCZOS).save("avatar_ES_con_asterisco.png")
# vista previa recortada en circulo, lado a lado
prev = Image.new("RGB", (1100, 560), (245, 245, 245))
for i, f in enumerate(["avatar_EN_with_an_asterisk.png", "avatar_ES_con_asterisco.png"]):
    im = Image.open(f).resize((480, 480), Image.LANCZOS)
    m = Image.new("L", (480 * 4, 480 * 4), 0); ImageDraw.Draw(m).ellipse([0, 0, 480 * 4, 480 * 4], fill=255)
    prev.paste(im, (40 + i * 540, 40), m.resize((480, 480), Image.LANCZOS))
prev.save("preview.png")
print("ok")
