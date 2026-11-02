"""Une la plantilla con la foto y genera invitacion_zoe.html."""
import base64

from PIL import Image

foto = Image.open("blancanieves_cachetes_suaves.png").convert("RGB").resize((1400, 1400), Image.LANCZOS)
foto.save("zoe_foto.webp", "WEBP", quality=86)
t = open("zoe_plantilla.html", encoding="utf8").read()
t = t.replace("__FOTO__", "data:image/webp;base64," + base64.b64encode(open("zoe_foto.webp", "rb").read()).decode())
open("invitacion_zoe.html", "w", encoding="utf8", newline="\n").write(t)
print(len(t))
