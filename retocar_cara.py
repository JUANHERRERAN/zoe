"""Amplia la imagen de Blancanieves bebe y embellece la cara con retoques suaves."""
import sys

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter

entrada, salida = sys.argv[1], sys.argv[2]
S = 8  # factor de ampliacion; las coordenadas estan en pixeles de la imagen original
ALTO_FINAL = 1920  # lado largo de Full HD

base = Image.open(entrada).convert("RGB")
W, H = base.width * S, base.height * S
img = base.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=8, percent=60, threshold=2))

OJO_I = (87.0, 116.5)
OJO_D = (122.5, 116.0)


def ojos_mas_grandes(im, centros, radio, fuerza):
    a = np.asarray(im).astype(np.float32)
    yy, xx = np.mgrid[:a.shape[0], :a.shape[1]].astype(np.float32)
    sx, sy = xx.copy(), yy.copy()
    for cx, cy in centros:
        cx, cy, R = cx * S, cy * S, radio * S
        dx, dy = xx - cx, yy - cy
        r = np.clip(np.hypot(dx, dy) / R, 0, 1)
        f = 1 - fuerza * (1 - r) ** 2
        dentro = r < 1
        sx[dentro] = (cx + dx * f)[dentro]
        sy[dentro] = (cy + dy * f)[dentro]
    x0 = np.clip(sx.astype(np.int32), 0, a.shape[1] - 2)
    y0 = np.clip(sy.astype(np.int32), 0, a.shape[0] - 2)
    fx, fy = (sx - x0)[..., None], (sy - y0)[..., None]
    res = (a[y0, x0] * (1 - fx) + a[y0, x0 + 1] * fx) * (1 - fy) + (a[y0 + 1, x0] * (1 - fx) + a[y0 + 1, x0 + 1] * fx) * fy
    return Image.fromarray(np.clip(res, 0, 255).astype(np.uint8))


def caja(cx, cy, rx, ry):
    return [(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S]


def elipse_suave(cx, cy, rx, ry, difumina):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).ellipse(caja(cx, cy, rx, ry), fill=255)
    return m.filter(ImageFilter.GaussianBlur(difumina * S))


def pintar(im, color, mascara, alfa):
    capa = Image.new("RGB", (W, H), color)
    return Image.composite(capa, im, mascara.point(lambda v: int(v * alfa)))


# 1. Ojos un poco mas grandes
img = ojos_mas_grandes(img, [OJO_I, OJO_D], radio=19, fuerza=0.17)

# 2. Piel pareja solo en mejillas y barbilla, sin llegar al flequillo
piel = elipse_suave(105, 127, 30, 18, 2.4)
excluir = Image.new("L", (W, H), 0)
de = ImageDraw.Draw(excluir)
for cx, cy in (OJO_I, OJO_D):
    de.ellipse(caja(cx, cy, 14.5, 13), fill=255)
de.ellipse(caja(105, 135, 10.5, 8), fill=255)
de.ellipse(caja(105, 124, 5.5, 4), fill=255)
excluir = excluir.filter(ImageFilter.GaussianBlur(1.3 * S))
piel = ImageChops.subtract(piel, excluir)
img = Image.composite(img.filter(ImageFilter.GaussianBlur(2.6 * S)), img, piel.point(lambda v: int(v * 0.8)))
img = pintar(img, (255, 226, 214), piel, 0.26)

# 3. Rubor rosado y luz en las mejillas
for cx, cy in ((78, 129), (131.5, 128)):
    img = pintar(img, (255, 138, 156), elipse_suave(cx, cy, 8.5, 5, 3), 0.3)
    img = pintar(img, (255, 255, 255), elipse_suave(cx - 3, cy - 2.6, 2.2, 1.1, 0.8), 0.4)

# 4. Ojos: mirada mas nitida, reflejo calido abajo y brillos claros arriba
ojos = Image.new("L", (W, H), 0)
do = ImageDraw.Draw(ojos)
for cx, cy in (OJO_I, OJO_D):
    do.ellipse(caja(cx, cy, 9.5, 8.5), fill=255)
ojos = ojos.filter(ImageFilter.GaussianBlur(1.3 * S))
nitido = img.filter(ImageFilter.UnsharpMask(radius=7, percent=70, threshold=0))
img = Image.composite(nitido, img, ojos)
for cx, cy in (OJO_I, OJO_D):
    img = pintar(img, (168, 96, 46), elipse_suave(cx, cy + 5, 6.8, 3, 1.1), 0.48)
    img = pintar(img, (255, 255, 255), elipse_suave(cx + 3.4, cy - 3.2, 2.1, 2.3, 0.14), 0.97)
    img = pintar(img, (255, 255, 255), elipse_suave(cx - 3.8, cy + 3.5, 1.1, 1.1, 0.12), 0.88)

# 5. Boca: mismo dibujo, con mas definicion y un tono mas alegre
boca = elipse_suave(105, 135.5, 7.5, 5, 1.2)
viva = ImageEnhance.Color(img.filter(ImageFilter.UnsharpMask(radius=7, percent=50, threshold=0))).enhance(1.12)
img = Image.composite(viva, img, boca)
img = pintar(img, (255, 255, 255), elipse_suave(105, 139.4, 2, 0.55, 0.3), 0.32)

# 6. Toque de luz en la nariz
img = pintar(img, (255, 255, 255), elipse_suave(104.4, 122.8, 1.6, 1, 0.45), 0.6)

final = img.resize((round(W * ALTO_FINAL / H), ALTO_FINAL), Image.LANCZOS)
final.save(salida)
print("final", final.size)

# Comparacion para revisar
b = (55, 85, 165, 155)
a1 = base.crop(b).resize(((b[2] - b[0]) * 5, (b[3] - b[1]) * 5), Image.BICUBIC)
a2 = img.crop(tuple(v * S for v in b)).resize(a1.size, Image.LANCZOS)
comp = Image.new("RGB", (a1.width * 2 + 12, a1.height), (120, 120, 120))
comp.paste(a1, (0, 0))
comp.paste(a2, (a1.width + 12, 0))
comp.save(sys.argv[3])
print(img.size)
