"""Quita hojas, flores y el boton del fondo y deja a la leona intacta."""
import sys

import numpy as np
from PIL import Image, ImageDraw

entrada, salida = sys.argv[1], sys.argv[2]
im = Image.open(entrada).convert("RGB")
arr = np.asarray(im).astype(np.int16)
r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
alto, ancho = r.shape

# Silueta holgada de la leona: todo lo que quede fuera es fondo seguro.
SILUETA = [
    (238, 125), (250, 92), (265, 78), (302, 95), (440, 112), (490, 100),
    (525, 122), (534, 160), (520, 213), (468, 238), (455, 240), (428, 272),
    (456, 322), (505, 366), (546, 398), (537, 425), (537, 454), (146, 454),
    (147, 415), (170, 368), (186, 300), (184, 245), (172, 225), (150, 222),
    (125, 234), (118, 255), (111, 280), (103, 280), (90, 222), (100, 190),
    (125, 165), (155, 163), (187, 190), (198, 222), (213, 265), (213, 300),
    (198, 350), (235, 342), (272, 296), (290, 278), (288, 268), (272, 255),
    (258, 238), (250, 212), (254, 188), (246, 168),
]
lienzo = Image.new("L", (ancho, alto), 0)
ImageDraw.Draw(lienzo).polygon(SILUETA, fill=255)
dentro = np.asarray(lienzo) > 0


def dilatar(mask):
    n = mask.copy()
    n[1:, :] |= mask[:-1, :]
    n[:-1, :] |= mask[1:, :]
    n[:, 1:] |= mask[:, :-1]
    n[:, :-1] |= mask[:, 1:]
    return n


# Lo que frena el relleno: el contorno oscuro y el pelaje color canela o crema.
contorno = (arr.max(axis=2) < 120) & ~(g > r + 5)
pelaje = (r > 150) & (r > g + 8) & (g > b + 20)
barrera = contorno | pelaje

# El fondo crece desde fuera de la silueta hasta chocar con la leona.
fondo = ~dentro
while True:
    nuevo = dilatar(fondo) & ~barrera | fondo
    if (nuevo == fondo).all():
        break
    fondo = nuevo

# Un pixel mas para borrar el halo verde que deja el borde difuminado.
fondo |= dilatar(fondo) & ~barrera

# Encima de la cabeza el fondo ya es blanco: la corona y sus flores no se tocan.
fondo[:140, 295:450] = False

res = arr.copy()
res[fondo] = 255
Image.fromarray(res.astype(np.uint8)).save(salida)
print("pixeles de fondo", int(fondo.sum()), "de", alto * ancho)
