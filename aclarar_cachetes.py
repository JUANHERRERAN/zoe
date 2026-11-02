"""Baja el rojo de los cachetes acercandolos al tono de la piel, sin tocar labios ni nariz."""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

entrada, salida, comparar = sys.argv[1], sys.argv[2], sys.argv[3]
QUITAR = 0.3  # parte del exceso de rojo que se elimina
LADO_FINAL = 1920

base = Image.open(entrada).convert("RGB")
W, H = base.size
a = np.asarray(base).astype(np.float32)


def mascara(elipses, difumina):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    for cx, cy, rx, ry in elipses:
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=255)
    return np.asarray(m.filter(ImageFilter.GaussianBlur(difumina))).astype(np.float32) / 255


zona = mascara([(295, 356, 60, 52), (446, 352, 58, 50)], 10)
excluir = mascara([(372, 372, 30, 21), (370, 335, 20, 17)], 4)
peso = zona * (1 - excluir)

# Tono de piel de referencia: la frente, donde no hay rubor
piel = np.median(a[215:250, 345:395].reshape(-1, 3), axis=0)
print("piel", piel)

r, g, b = a[..., 0], a[..., 1], a[..., 2]
# El exceso de rojo se mide contra la piel; el negro y el blanco de los ojos no lo tienen
exceso_g = np.clip((r - g) - (piel[0] - piel[1]), 0, None)
exceso_b = np.clip((r - b) - (piel[0] - piel[2]), 0, None)
piel_clara = r > 170
res = a.copy()
res[..., 1] = g + exceso_g * QUITAR * peso * piel_clara
res[..., 2] = b + exceso_b * QUITAR * peso * piel_clara

img = Image.fromarray(np.clip(res, 0, 255).astype(np.uint8))
img.resize((LADO_FINAL, LADO_FINAL), Image.LANCZOS).save(salida)

caja = (220, 180, 520, 440)
comp = Image.new("RGB", (612, 260), (120, 120, 120))
comp.paste(base.crop(caja), (0, 0))
comp.paste(img.crop(caja), (312, 0))
comp.resize((1224, 520), Image.LANCZOS).save(comparar)
