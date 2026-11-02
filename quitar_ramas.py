"""Quita las ramas y hojas verdes del fondo y deja al leon intacto."""
import sys

import numpy as np
from PIL import Image

entrada, salida = sys.argv[1], sys.argv[2]
arr = np.asarray(Image.open(entrada).convert("RGB")).astype(np.int16)
r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]


def dilatar(mask, pasos):
    m = mask.copy()
    for _ in range(pasos):
        n = m.copy()
        n[1:, :] |= m[:-1, :]
        n[:-1, :] |= m[1:, :]
        n[:, 1:] |= m[:, :-1]
        n[:, :-1] |= m[:, 1:]
        m = n
    return m


# Verde de hojas: incluye el amarillo verdoso claro y los contornos verde oscuro.
verde = (g >= r - 4) & (g > b + 12)
# Fondo casi blanco y neutro.
claro = (arr.min(axis=2) > 205) & (arr.max(axis=2) - arr.min(axis=2) < 22)
# Leon, corona y cola: tonos calidos donde el rojo domina claramente.
calido = (r > g + 10) & (r > b + 10)

# Zona de hojas: el verde mas su borde, sin invadir los tonos calidos.
zona = dilatar(verde, 3) & ~calido

# El contorno oscuro del leon queda protegido si toca tonos calidos y no verdes.
oscuro = arr.max(axis=2) < 110
contorno_leon = oscuro & dilatar(calido, 3) & ~dilatar(verde, 1)
zona &= ~contorno_leon

# Restos pequenos: pixeles no claros rodeados de zona ya eliminada.
for _ in range(3):
    zona |= dilatar(zona, 1) & ~calido & ~contorno_leon & ~claro

# La corona y los ojos tienen brillos amarillos que parecen hoja: no se tocan.
zona[:385, :] = False
zona[390:530, 100:350] = False

alto, ancho = zona.shape
yy, xx = np.mgrid[:alto, :ancho]

# Restos sueltos de hoja encima del lomo.
zona[655:692, 505:548] = True

# Tallo marron de la rama, entre (590, 697) y (530, 800).
px, py, qx, qy = 590, 697, 530, 800
t = np.clip(((xx - px) * (qx - px) + (yy - py) * (qy - py)) / ((qx - px) ** 2 + (qy - py) ** 2), 0, 1)
dist = np.hypot(xx - (px + t * (qx - px)), yy - (py + t * (qy - py)))
zona |= (dist < 7) & (xx > 529)

# Puntos sueltos del fondo: lejos del leon y sin tonos calidos fuertes.
zona[700:790, 530:600] = True
zona[825:840, 50:65] = True

# Fondo uniforme: se extiende desde los bordes para que no queden manchas.
libre = claro | zona
fuera = np.zeros_like(libre)
fuera[0, :] = fuera[-1, :] = fuera[:, 0] = fuera[:, -1] = True
fuera &= libre
while True:
    nuevo = dilatar(fuera, 1) & libre
    if (nuevo == fuera).all():
        break
    fuera = nuevo
zona |= fuera

fondo = np.median(arr[claro], axis=0)
res = arr.copy()
res[zona] = fondo

Image.fromarray(res.astype(np.uint8)).save(salida)
print("tamano", arr.shape[1], "x", arr.shape[0], "fondo", fondo, "pixeles cambiados", int(zona.sum()))
