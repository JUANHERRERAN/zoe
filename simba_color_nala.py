"""Pinta el pelaje de Simba con los tonos del pelaje de Nala."""
import sys

import numpy as np
from PIL import Image

simba_ruta, nala_ruta, salida = sys.argv[1], sys.argv[2], sys.argv[3]
simba = np.asarray(Image.open(simba_ruta).convert("RGB")).astype(np.float32)
nala = np.asarray(Image.open(nala_ruta).convert("RGB")).astype(np.float32)


def luz(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


# Tonos de Nala: pelaje canela o crema, sin la corona ni las florecitas.
r, g, b = nala[..., 0], nala[..., 1], nala[..., 2]
pelaje_nala = (r > 150) & (r > g + 8) & (g > b + 20)
pelaje_nala[:140, :] = False
# Tampoco el gris topo de las orejas ni el marron de la cola, que no son su pelaje.
pelaje_nala[100:190, 250:300] = False
pelaje_nala[130:235, 450:525] = False
pelaje_nala[160:290, 85:200] = False
tonos = nala[pelaje_nala]
tonos = tonos[np.argsort(luz(tonos))]

# Pelaje de Simba: naranja o crema, no oscuro y sin rojos de nariz y boca.
r, g, b = simba[..., 0], simba[..., 1], simba[..., 2]
alto, ancho = r.shape
yy, xx = np.mgrid[:alto, :ancho]
L = luz(simba)
pelaje = (r > g + 6) & (g > b + 6) & (L > 75)
boca = (xx > 170) & (xx < 280) & (yy > 515) & (yy < 635)
pelaje &= ~(boca & (g < 130) & (b > 50))
# Nariz: sus sombras rojizas no llevan azul, asi que se separan por el verde.
pelaje &= ~(((xx - 218) ** 2 / 42 ** 2 + (yy - 540) ** 2 / 20 ** 2 < 1) & (g < 140))
# La corona baja un poco de izquierda a derecha; las orejas quedan a sus lados.
corona = (xx > 126) & (xx < 347) & (yy < 369 + (xx - 126) * 14 / 221)
pelaje &= ~corona
pelaje[:364, :] = False
pelaje[775:, 610:] = False
for cx, cy in ((151, 482), (305, 482)):
    ojo = (xx - cx) ** 2 + (yy - cy) ** 2 <= 33 ** 2
    # Dentro del ojo solo cambia el naranja vivo del parpado, no el iris.
    pelaje &= ~ojo | ((r > 190) & (b < 70) & (L > 100))

# Cada tono de Simba toma el de Nala con la misma posicion de claro a oscuro.
orden = np.argsort(L[pelaje])
pos = np.empty(orden.size, dtype=np.int64)
pos[orden] = np.arange(orden.size)
indice = (pos * (len(tonos) - 1) / max(orden.size - 1, 1)).astype(np.int64)
nuevo = tonos[indice]

# Suaviza el mapeo por luminosidad para que no aparezca ruido en el pelaje.
bins = 64
grupo = np.clip((L[pelaje] / 256 * bins).astype(np.int64), 0, bins - 1)
media = np.zeros((bins, 3), dtype=np.float32)
for i in range(bins):
    if (grupo == i).any():
        media[i] = nuevo[grupo == i].mean(axis=0)
validos = (media.sum(axis=1) > 0)
for c in range(3):
    media[:, c] = np.interp(np.arange(bins), np.flatnonzero(validos), media[validos, c])

res = simba.copy()
res[pelaje] = media[grupo]
Image.fromarray(np.clip(res, 0, 255).astype(np.uint8)).save(salida)
print("tonos de Nala", len(tonos), "pixeles de pelaje", orden.size)
