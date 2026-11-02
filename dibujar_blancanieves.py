"""Genera a Blancanieves bebe como SVG detallado, con destellos repartidos al azar."""
import math
import random

random.seed(26)

# Formas que se usan como relleno y como recorte
FALDA = "M228 528C170 585 120 640 106 686c22 28 62 14 94 26 35 14 65-6 100 4 35-10 65 10 100-4 32-12 72 2 94-26-14-46-64-101-122-158-47 24-97 24-144 0Z"
CORPINO = "M238 424q62 12 124 0l20 110q-82 32-164 0Z"
MANGA = "M240 428C205 402 148 410 128 452c-18 38-2 76 24 84 23 9 60 4 84-12 12-29 14-66 4-96Z"
CARA = "M300 146C204 146 148 210 148 292c0 84 66 138 152 138s152-54 152-138c0-82-56-146-152-146Z"
PELO_FRENTE = "M302 116C190 112 124 186 134 304c5 20 13 30 24 34 3-60 42-116 92-154C264 204 290 212 316 212C372 206 432 214 442 338c11-4 19-14 24-34C474 186 414 120 302 116Z"
PELO_ATRAS = "M300 104C136 104 100 238 116 342c8 60 52 96 94 84h180c42 12 86-24 94-84 16-104-20-238-184-238Z"


def petalos(r, n, giro, relleno, borde):
    s = []
    for i in range(n):
        a = giro + i * 360 / n
        s.append(
            f'<path transform="rotate({a:.0f})" fill="url(#{relleno})" stroke="{borde}" stroke-width="1.6" '
            f'd="M0 2C{-r*.8:.0f} {-r*.25:.0f} {-r*.72:.0f} {-r:.0f} 0 {-r:.0f}S{r*.8:.0f} {-r*.25:.0f} 0 2Z"/>'
        )
    return "".join(s)


def lentejuelas(n, x0, y0, x1, y1, colores, rmin, rmax):
    s = []
    for _ in range(n):
        s.append(
            f'<circle cx="{random.uniform(x0, x1):.1f}" cy="{random.uniform(y0, y1):.1f}" '
            f'r="{random.uniform(rmin, rmax):.1f}" fill="{random.choice(colores)}"/>'
        )
    return "".join(s)


def estrella(x, y, r, opacidad=1):
    c = r * 0.14
    return (
        f'<path filter="url(#halo)" opacity="{opacidad}" fill="#fff" d="M{x} {y-r}Q{x+c} {y-c} {x+r} {y}'
        f'Q{x+c} {y+c} {x} {y+r}Q{x-c} {y+c} {x-r} {y}Q{x-c} {y-c} {x} {y-r}Z"/>'
    )


def ojo(cx, cy, lado):
    # lado = -1 para el izquierdo, 1 para el derecho; las alas de las pestanas salen hacia fuera
    ala = lambda d: cx + lado * d
    return f"""
    <ellipse cx="{cx}" cy="{cy-34}" rx="44" ry="20" fill="#e88fa0" opacity=".28" filter="url(#blur6)"/>
    <ellipse cx="{cx}" cy="{cy}" rx="35" ry="42" fill="#fffdf9" stroke="#6b4030" stroke-width="1.5"/>
    <ellipse cx="{cx}" cy="{cy+3}" rx="30" ry="38" fill="url(#iris)" stroke="#2a1206" stroke-width="2.5"/>
    <ellipse cx="{cx}" cy="{cy+1}" rx="16" ry="22" fill="#170a03"/>
    <path d="M{cx-22} {cy+14}c8 20 36 20 44 0-8 10-36 10-44 0Z" fill="#ffc674" opacity=".85"/>
    <circle cx="{cx+10}" cy="{cy-15}" r="12" fill="#fff"/>
    <circle cx="{cx-11}" cy="{cy+15}" r="5.5" fill="#fff"/>
    <circle cx="{cx+13}" cy="{cy+8}" r="2.8" fill="#fff" opacity=".9"/>
    <path fill="#0d1520" d="M{cx-37} {cy-6}C{cx-30} {cy-48} {cx+30} {cy-48} {cx+37} {cy-6}C{cx+26} {cy-36} {cx-26} {cy-36} {cx-37} {cy-6}Z"/>
    <path fill="#0d1520" d="M{ala(32)} {cy-20}Q{ala(46)} {cy-26} {ala(52)} {cy-40}Q{ala(46)} {cy-16} {ala(35)} {cy-8}Z"/>
    <path fill="#0d1520" d="M{ala(35)} {cy-10}Q{ala(50)} {cy-12} {ala(58)} {cy-24}Q{ala(50)} {cy-4} {ala(36)} {cy}Z"/>
    <path fill="#0d1520" d="M{ala(24)} {cy-30}Q{ala(34)} {cy-42} {ala(36)} {cy-54}Q{ala(40)} {cy-38} {ala(30)} {cy-24}Z"/>
    <path fill="none" stroke="#a9694e" stroke-width="1.6" opacity=".45" stroke-linecap="round" d="M{cx-18} {cy+42}Q{cx} {cy+48} {cx+18} {cy+42}"/>
    <path fill="none" stroke="#a9694e" stroke-width="2" opacity=".6" stroke-linecap="round" d="M{cx-30} {cy-46}Q{cx} {cy-60} {cx+30} {cy-46}"/>
    """


svg = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 600 760" width="1200" height="1520" role="img" aria-label="Blancanieves bebe con corona y una rosa">
<defs>
  <linearGradient id="gPelo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1f3350"/><stop offset=".55" stop-color="#0f1c2e"/><stop offset="1" stop-color="#070d16"/></linearGradient>
  <linearGradient id="gBrillo" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#7fa8d6" stop-opacity="0"/><stop offset=".5" stop-color="#a9cdf0"/><stop offset="1" stop-color="#7fa8d6" stop-opacity="0"/></linearGradient>
  <radialGradient id="gPiel" cx=".5" cy=".42" r=".68"><stop offset="0" stop-color="#fff5ec"/><stop offset=".7" stop-color="#ffe6d5"/><stop offset="1" stop-color="#f8c9b0"/></radialGradient>
  <linearGradient id="gBrazo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff0e4"/><stop offset="1" stop-color="#f7c8ad"/></linearGradient>
  <radialGradient id="iris" cx=".5" cy=".78" r=".85"><stop offset="0" stop-color="#d98a34"/><stop offset=".5" stop-color="#8a4a1a"/><stop offset="1" stop-color="#2f1407"/></radialGradient>
  <radialGradient id="gCorpino" cx=".5" cy=".3" r=".85"><stop offset="0" stop-color="#6cb4ee"/><stop offset=".6" stop-color="#2f7bc6"/><stop offset="1" stop-color="#174f92"/></radialGradient>
  <linearGradient id="gFalda" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff0a0"/><stop offset=".45" stop-color="#ffd43f"/><stop offset="1" stop-color="#f4a81c"/></linearGradient>
  <radialGradient id="gManga" cx=".42" cy=".36" r=".72"><stop offset="0" stop-color="#ffffff"/><stop offset=".55" stop-color="#d9eeff"/><stop offset="1" stop-color="#86bdf0"/></radialGradient>
  <linearGradient id="gCuello" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#c8e2fa"/></linearGradient>
  <linearGradient id="gRojo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8fa0"/><stop offset=".6" stop-color="#ea3f5f"/><stop offset="1" stop-color="#b81f43"/></linearGradient>
  <linearGradient id="gOro" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff2a8"/><stop offset=".45" stop-color="#f7c52f"/><stop offset="1" stop-color="#b87a10"/></linearGradient>
  <radialGradient id="gRubi" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#ffb0bd"/><stop offset=".45" stop-color="#e01f4e"/><stop offset="1" stop-color="#7d0a28"/></radialGradient>
  <radialGradient id="gPetaloA" cx=".5" cy="1" r="1"><stop offset="0" stop-color="#d83e86"/><stop offset=".7" stop-color="#f76fae"/><stop offset="1" stop-color="#ffc0dc"/></radialGradient>
  <radialGradient id="gPetaloB" cx=".5" cy="1" r="1"><stop offset="0" stop-color="#c22c75"/><stop offset="1" stop-color="#ff8cc0"/></radialGradient>
  <linearGradient id="gHoja" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8bdc72"/><stop offset="1" stop-color="#2c8f3c"/></linearGradient>
  <linearGradient id="gZapato" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f24a6c"/><stop offset="1" stop-color="#a8133a"/></linearGradient>
  <linearGradient id="gLabio" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7396"/><stop offset="1" stop-color="#e8466f"/></linearGradient>
  <radialGradient id="gCachete" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff7f98" stop-opacity=".62"/><stop offset="1" stop-color="#ff7f98" stop-opacity="0"/></radialGradient>
  <filter id="blur3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
  <filter id="blur6" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="blur12" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="12"/></filter>
  <filter id="halo" x="-120%" y="-120%" width="340%" height="340%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="cFalda"><path d="{FALDA}"/></clipPath>
  <clipPath id="cCorpino"><path d="{CORPINO}"/></clipPath>
  <clipPath id="cCara"><path d="{CARA}"/></clipPath>
  <clipPath id="cFrente"><path d="{PELO_FRENTE}"/></clipPath>
  <clipPath id="cAtras"><path d="{PELO_ATRAS}"/></clipPath>
  <clipPath id="cManga"><path d="{MANGA}"/></clipPath>
  <g id="manga">
    <path d="{MANGA}" fill="url(#gManga)" fill-opacity=".97" stroke="#5b95cf" stroke-width="2.5"/>
    <g clip-path="url(#cManga)">
      <path d="M168 432c-16 26-18 58-4 82 18-20 22-58 4-82Z" fill="url(#gRojo)" stroke="#fff" stroke-width="2"/>
      <path d="M214 428c-14 28-14 62 0 86 16-24 18-60 0-86Z" fill="url(#gRojo)" stroke="#fff" stroke-width="2"/>
      <path d="M140 462c-6 22-4 42 6 58 10-20 8-42-6-58Z" fill="url(#gRojo)" stroke="#fff" stroke-width="1.6" opacity=".9"/>
      <path fill="none" stroke="#8fc0ee" stroke-width="2" d="M190 420c-4 32-4 72 4 118M238 440c-8 30-10 60-6 90M150 430c-10 26-12 60-4 96"/>
      <ellipse cx="170" cy="444" rx="34" ry="14" fill="#fff" opacity=".85" filter="url(#blur6)"/>
    </g>
    <path d="M146 524c28 20 68 20 96-2l-6 22c-28 18-62 20-88 4Z" fill="url(#gOro)" stroke="#9a6a10" stroke-width="2"/>
    <path fill="none" stroke="#fff4b8" stroke-width="2" d="M152 534c26 14 56 14 82-2"/>
  </g>
  <g id="cuello">
    <path d="M232 434c-28-22-36-54-24-84 26 28 56 58 80 78l-36 50c-8-16-16-30-20-44Z" fill="url(#gCuello)" stroke="#7fb0e0" stroke-width="2.5"/>
    <path fill="none" stroke="#a9d0f2" stroke-width="2" d="M222 402c14 12 30 24 44 32"/>
  </g>
</defs>

<!-- Zapatitos -->
<g stroke="#7a0d2a" stroke-width="2.5">
  <ellipse cx="244" cy="724" rx="44" ry="24" fill="url(#gZapato)"/>
  <ellipse cx="356" cy="724" rx="44" ry="24" fill="url(#gZapato)"/>
</g>
<ellipse cx="232" cy="716" rx="16" ry="6" fill="#fff" opacity=".6" filter="url(#blur3)"/>
<ellipse cx="344" cy="716" rx="16" ry="6" fill="#fff" opacity=".6" filter="url(#blur3)"/>

<!-- Falda -->
<path d="{FALDA}" fill="url(#gFalda)" stroke="#b97c12" stroke-width="2.5"/>
<g clip-path="url(#cFalda)">
  <g fill="none" stroke="#d98a10" stroke-width="16" opacity=".5" filter="url(#blur6)">
    <path d="M250 560c-18 50-44 100-66 150M300 570v150M350 560c18 50 44 100 66 150M214 560c-30 44-60 90-82 130M386 560c30 44 60 90 82 130"/>
  </g>
  <g fill="none" stroke="#fff6b8" stroke-width="12" opacity=".75" filter="url(#blur6)">
    <path d="M272 566c-10 46-24 96-36 146M328 566c10 46 24 96 36 146M186 610c-20 30-38 58-50 84M414 610c20 30 38 58 50 84"/>
  </g>
  <path d="M228 528c47 26 97 26 144 0v12c-47 26-97 26-144 0Z" fill="#c9860f" opacity=".45" filter="url(#blur3)"/>
  {lentejuelas(170, 110, 545, 490, 720, ["#ffffff", "#fff7c2", "#ffe680"], 0.7, 2.2)}
</g>

<!-- Brazos -->
<path d="M160 540c-20 22-34 44-40 66-4 26 30 36 44 14 8-22 20-48 36-76Z" fill="url(#gBrazo)" stroke="#b97a5c" stroke-width="2.2"/>
<path d="M440 540c20 22 34 46 36 70 2 26-34 32-44 10-6-24-16-50-32-76Z" fill="url(#gBrazo)" stroke="#b97a5c" stroke-width="2.2"/>
<path d="M430 612c-4 14 2 28 16 32 16 4 30-6 32-22 1-16-10-28-24-28-12 0-22 8-24 18Z" fill="url(#gBrazo)" stroke="#b97a5c" stroke-width="2.2"/>
<path fill="none" stroke="#b97a5c" stroke-width="2" stroke-linecap="round" d="M448 640c-2-8-2-14 0-20M460 642c0-8 0-14 2-20M470 636c2-6 2-12 2-16"/>

<!-- Corpino -->
<path d="{CORPINO}" fill="url(#gCorpino)" stroke="#123f78" stroke-width="2.5"/>
<g clip-path="url(#cCorpino)">
  {lentejuelas(230, 215, 420, 385, 560, ["#ffffff", "#bfe2ff", "#7fc0f5", "#1c5aa4"], 0.8, 2)}
  <path d="M218 430c10 40 12 80 4 110M382 430c-10 40-12 80-4 110" fill="none" stroke="#0f3a70" stroke-width="16" opacity=".4" filter="url(#blur6)"/>
</g>
<path d="M300 476v78" fill="none" stroke="#b87a10" stroke-width="7" stroke-linecap="round"/>
<path d="M300 476v78" fill="none" stroke="#ffe27a" stroke-width="3.5" stroke-linecap="round"/>

<!-- Escote -->
<path d="M258 416h84l-14 58q-28 16-56 0Z" fill="url(#gBrazo)" stroke="#b97a5c" stroke-width="2"/>
<path d="M258 424h84l-6 24q-36 14-72 0Z" fill="#d98f73" opacity=".45" filter="url(#blur6)"/>

<!-- Cuello y mangas -->
<use xlink:href="#cuello" href="#cuello"/>
<use xlink:href="#cuello" href="#cuello" transform="translate(600 0) scale(-1 1)"/>
<use xlink:href="#manga" href="#manga"/>
<use xlink:href="#manga" href="#manga" transform="translate(600 0) scale(-1 1)"/>
<g fill="#fff">{lentejuelas(46, 130, 420, 240, 530, ["#ffffff"], 0.7, 1.8)}{lentejuelas(46, 360, 420, 470, 530, ["#ffffff"], 0.7, 1.8)}</g>

<!-- Rosa -->
<path d="M146 616c-6-50-18-96-36-136" fill="none" stroke="#1f7a33" stroke-width="10" stroke-linecap="round"/>
<path d="M146 616c-6-50-18-96-36-136" fill="none" stroke="#5cc25f" stroke-width="5" stroke-linecap="round"/>
<g stroke="#1f7a33" stroke-width="2">
  <path d="M136 566c-28-12-52-4-66 22 28 12 52 4 66-22Z" fill="url(#gHoja)"/>
  <path d="M124 512c22-20 46-20 64-4-18 22-44 22-64 4Z" fill="url(#gHoja)"/>
</g>
<path d="M132 568c-18 2-34 10-52 18M130 511c16 0 32 0 50-2" fill="none" stroke="#1f7a33" stroke-width="1.6"/>
<g transform="translate(106 442)">
  <circle r="44" fill="#d83e86" opacity=".4" filter="url(#blur12)"/>
  {petalos(50, 6, 20, "gPetaloA", "#b52a70")}
  {petalos(36, 5, 50, "gPetaloB", "#a81f64")}
  {petalos(23, 4, 15, "gPetaloA", "#a81f64")}
  <circle r="11" fill="#c22c75" stroke="#8e1a55" stroke-width="1.5"/>
  <path d="M-6 2c2-8 12-8 13 0 0 6-8 8-10 2" fill="none" stroke="#ffd2e6" stroke-width="2" stroke-linecap="round"/>
  <ellipse cx="-20" cy="-24" rx="14" ry="7" fill="#fff" opacity=".55" filter="url(#blur3)" transform="rotate(-35 -20 -24)"/>
</g>
<!-- Mano que sostiene la rosa -->
<path d="M122 610c-4 16 6 30 22 32 16 2 30-10 30-26 0-14-12-26-26-26-12 0-23 8-26 20Z" fill="url(#gBrazo)" stroke="#b97a5c" stroke-width="2.2"/>
<path fill="none" stroke="#b97a5c" stroke-width="2" stroke-linecap="round" d="M128 604c8 2 16 4 22 4M126 616c8 2 18 4 26 2M132 628c6 2 14 2 22 0"/>

<!-- Cabeza, ligeramente inclinada -->
<g transform="rotate(-4 300 430)">
  <!-- Pelo de atras y mono -->
  <circle cx="458" cy="180" r="48" fill="url(#gPelo)" stroke="#060b13" stroke-width="2.5"/>
  <path d="M436 158c14-14 36-10 46 6" fill="none" stroke="#6f95bd" stroke-width="6" stroke-linecap="round" opacity=".7" filter="url(#blur3)"/>
  <path d="{PELO_ATRAS}" fill="url(#gPelo)" stroke="#060b13" stroke-width="2.5"/>
  <g clip-path="url(#cAtras)" fill="none" stroke="#2c4667" stroke-width="2.5" opacity=".8">
    <path d="M130 300c0 50 20 90 60 118M108 330c8 50 30 84 70 96M470 300c0 50-20 90-60 118M492 330c-8 50-30 84-70 96"/>
  </g>

  <!-- Cara -->
  <path d="{CARA}" fill="url(#gPiel)" stroke="#b97a5c" stroke-width="2.2"/>
  <g clip-path="url(#cCara)">
    <path d="{PELO_FRENTE}" fill="#8a4f35" opacity=".38" transform="translate(0 12)" filter="url(#blur6)"/>
    <ellipse cx="196" cy="364" rx="50" ry="36" fill="url(#gCachete)"/>
    <ellipse cx="404" cy="364" rx="50" ry="36" fill="url(#gCachete)"/>
  </g>
  <ellipse cx="184" cy="350" rx="11" ry="6" fill="#fff" opacity=".8" filter="url(#blur3)"/>
  <ellipse cx="392" cy="350" rx="11" ry="6" fill="#fff" opacity=".8" filter="url(#blur3)"/>
  <ellipse cx="300" cy="228" rx="40" ry="20" fill="#fff" opacity=".55" filter="url(#blur12)"/>

  {ojo(232, 312, -1)}
  {ojo(368, 312, 1)}

  <!-- Cejas -->
  <path fill="#1a1a24" d="M196 252c14-16 40-20 62-10-22-4-44 0-60 14Z"/>
  <path fill="#1a1a24" d="M404 252c-14-16-40-20-62-10 22-4 44 0 60 14Z"/>

  <!-- Nariz -->
  <ellipse cx="300" cy="358" rx="15" ry="9" fill="#e9a78d" opacity=".55" filter="url(#blur3)"/>
  <path d="M291 360c6 6 12 6 18 0" fill="none" stroke="#c98468" stroke-width="2.6" stroke-linecap="round"/>
  <circle cx="297" cy="350" r="3" fill="#fff" opacity=".9"/>

  <!-- Boca -->
  <path d="M270 381q30 12 60 0" fill="none" stroke="#c9566f" stroke-width="1.8" opacity=".55" stroke-linecap="round"/>
  <path d="M280 384c6-4 12-6 16-5 2 0 3 2 4 3 1-1 2-3 4-3 4-1 10 1 16 5-13 6-27 6-40 0Z" fill="url(#gLabio)" stroke="#c23a60" stroke-width="1.4"/>
  <path d="M283 386c11 5 23 5 34 0-3 13-10 18-17 18s-14-5-17-18Z" fill="url(#gLabio)" stroke="#c23a60" stroke-width="1.4"/>
  <ellipse cx="300" cy="395" rx="8" ry="3" fill="#ffd6e0" filter="url(#blur3)"/>

  <!-- Pelo de delante -->
  <path d="{PELO_FRENTE}" fill="url(#gPelo)" stroke="#060b13" stroke-width="2.5"/>
  <g clip-path="url(#cFrente)">
    <path d="M152 262c14-50 54-92 108-112" fill="none" stroke="url(#gBrillo)" stroke-width="30" opacity=".75" filter="url(#blur6)"/>
    <path d="M334 138c52 12 96 50 112 104" fill="none" stroke="url(#gBrillo)" stroke-width="30" opacity=".75" filter="url(#blur6)"/>
    <g fill="none" stroke="#3f5f86" stroke-width="2" opacity=".85">
      <path d="M166 310c2-60 34-112 86-146M150 306c0-70 40-132 104-162M186 262c14-36 36-62 66-82"/>
      <path d="M284 148c52 22 118 60 148 158M300 134c60 18 128 70 144 158M272 172c56 22 112 46 142 92"/>
    </g>
  </g>
  <!-- Ricito -->
  <path d="M250 184c-10-24 2-48 28-54-14 12-20 28-14 44 2 6 2 10-2 14Z" fill="url(#gPelo)" stroke="#060b13" stroke-width="2.2"/>

  <!-- Corona -->
  <g stroke="#8f5e0c" stroke-width="2.2" stroke-linejoin="round">
    <path d="M224 144l-12-52 40 30 8-48 28 34 12-54 12 54 28-34 8 48 40-30-12 52c-48-20-104-20-152 0Z" fill="url(#gOro)"/>
    <path d="M222 148c50-22 106-22 156 0l-2 14c-50-20-102-20-152 0Z" fill="url(#gOro)"/>
    <circle cx="212" cy="90" r="9" fill="url(#gOro)"/>
    <circle cx="260" cy="72" r="8" fill="url(#gOro)"/>
    <circle cx="300" cy="50" r="10" fill="url(#gOro)"/>
    <circle cx="340" cy="72" r="8" fill="url(#gOro)"/>
    <circle cx="388" cy="90" r="9" fill="url(#gOro)"/>
  </g>
  <g stroke="#6e0a24" stroke-width="1.8">
    <path d="M300 92l17 22-17 22-17-22Z" fill="url(#gRubi)"/>
    <ellipse cx="256" cy="126" rx="11" ry="13" fill="url(#gRubi)"/>
    <ellipse cx="344" cy="126" rx="11" ry="13" fill="url(#gRubi)"/>
  </g>
  <path d="M292 108l6-6M250 120l4-4M338 120l4-4" stroke="#fff" stroke-width="3" stroke-linecap="round"/>
  <g fill="#fff6c4">{"".join(f'<circle cx="{232 + i * 15.5:.0f}" cy="{155 - 7 * math.sin(i * math.pi / 9):.0f}" r="2.2"/>' for i in range(10))}</g>
  {estrella(300, 50, 22)}
  {estrella(214, 88, 13, .95)}
  {estrella(388, 88, 13, .95)}
  {estrella(300, 114, 12, .95)}
  {estrella(216, 196, 10, .9)}
  {estrella(420, 214, 11, .9)}
</g>

<!-- Destellos -->
{estrella(250, 492, 13)}
{estrella(346, 516, 11)}
{estrella(172, 462, 13)}
{estrella(430, 448, 13)}
{estrella(216, 640, 15)}
{estrella(400, 618, 14)}
{estrella(310, 672, 11)}
{estrella(84, 412, 13)}
{estrella(136, 660, 8)}
</svg>
"""

with open("blancanieves_bebe.svg", "w", encoding="utf8", newline="\n") as f:
    f.write(svg)
print(len(svg))
