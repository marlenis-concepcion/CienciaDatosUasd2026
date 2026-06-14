from pathlib import Path
from textwrap import wrap

from docx import Document
from PIL import Image, ImageDraw, ImageFont


GENERAL = Path(__file__).resolve().parents[1]
DOCUMENTS = GENERAL / "Documentos_Academicos"
ASSETS = GENERAL / "Recursos_Visuales"
DOCX = DOCUMENTS / "Ensayo1_MarlenisConcepcion40225495809.docx"
PDF = DOCUMENTS / "Ensayo1_MarlenisConcepcion40225495809.pdf"
LOGO = ASSETS / "uasd_logo.png"
TIMELINE = ASSETS / "figura_1_linea_tiempo_dsc.png"
QR = ASSETS / "anexo_qr_linea_tiempo_dsc.png"

W, H = 1700, 2200
M = 200
BLUE = (0, 89, 160)
TEAL = (27, 154, 170)
GOLD = (242, 183, 5)
BLACK = (20, 20, 20)
GRAY = (245, 245, 245)
LIGHT_BLUE = (234, 246, 252)
LIGHT_GOLD = (255, 244, 204)

FONT_DIR = Path("/System/Library/Fonts/Supplemental")
FONT = FONT_DIR / "Times New Roman.ttf"
FONT_BOLD = FONT_DIR / "Times New Roman Bold.ttf"
FONT_ITALIC = FONT_DIR / "Times New Roman Italic.ttf"


def font(size, bold=False, italic=False):
    path = FONT_BOLD if bold else FONT_ITALIC if italic else FONT
    return ImageFont.truetype(str(path), size)


F12 = font(34)
F12B = font(34, bold=True)
F12I = font(34, italic=True)
F10 = font(28)
F14B = font(40, bold=True)
F15B = font(44, bold=True)


def roman(n):
    vals = [(10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    out = ""
    for val, sym in vals:
        while n >= val:
            out += sym
            n -= val
    return out


class PdfBuilder:
    def __init__(self):
        self.pages = []
        self.page = None
        self.draw = None
        self.y = M
        self.mode = "none"
        self.num = 0

    def new_page(self, mode=None):
        if self.page is not None:
            self.pages.append(self.page)
        if mode is not None:
            self.mode = mode
            self.num = 1
        elif self.mode != "none":
            self.num += 1
        self.page = Image.new("RGB", (W, H), "white")
        self.draw = ImageDraw.Draw(self.page)
        self.y = M
        if self.mode == "roman":
            self.draw.text((W - M, 90), roman(self.num), fill=BLACK, font=F12, anchor="ra")
        elif self.mode == "arabic":
            self.draw.text((W - M, 90), str(self.num), fill=BLACK, font=F12, anchor="ra")

    def finish(self):
        if self.page is not None:
            self.pages.append(self.page)
        first, rest = self.pages[0], self.pages[1:]
        first.save(PDF, "PDF", resolution=200, save_all=True, append_images=rest)

    def ensure(self, need):
        if self.y + need > H - M:
            self.new_page()

    def text_width(self, text, fnt):
        return self.draw.textbbox((0, 0), text, font=fnt)[2]

    def lines(self, text, fnt, width, indent=0):
        words = text.split()
        lines, cur = [], ""
        for word in words:
            test = word if not cur else cur + " " + word
            if self.text_width(test, fnt) <= width - indent:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines or [""]

    def paragraph(self, text, fnt=F12, bold=False, italic=False, center=False, indent=True, color=BLACK, after=26):
        if not text.strip():
            self.y += 50
            return
        use_font = F12B if bold else F12I if italic else fnt
        width = W - (2 * M)
        first_indent = 75 if indent and not center else 0
        lines = self.lines(text, use_font, width, first_indent)
        line_h = 64
        self.ensure(line_h * len(lines) + after)
        for i, line in enumerate(lines):
            x = W // 2 if center else M + (first_indent if i == 0 else 0)
            anchor = "ma" if center else "la"
            self.draw.text((x, self.y), line, fill=color, font=use_font, anchor=anchor)
            self.y += line_h
        self.y += after

    def heading(self, text, level=1):
        self.paragraph(text, F12B, bold=True, center=(level == 1), indent=False, after=22)

    def image(self, path, max_w, after=26):
        if not path.exists():
            return
        img = Image.open(path).convert("RGB")
        ratio = max_w / img.width
        img = img.resize((int(img.width * ratio), int(img.height * ratio)))
        self.ensure(img.height + after)
        self.page.paste(img, ((W - img.width) // 2, self.y))
        self.y += img.height + after


def cover(pdf):
    pdf.new_page("none")
    pdf.y = 185
    pdf.image(LOGO, 230, after=30)
    pdf.paragraph("Presentación", F14B, bold=True, center=True, indent=False, color=BLUE, after=18)
    pdf.paragraph("Universidad Autónoma de Santo Domingo (UASD)", F15B, bold=True, center=True, indent=False, color=BLUE, after=18)
    pdf.paragraph("Facultad de Ciencias", F12B, bold=True, center=True, indent=False, color=TEAL, after=16)
    pdf.paragraph("Programa de Maestría", F12, center=True, indent=False, after=22)
    pdf.paragraph("Ensayo 1", F14B, bold=True, center=True, indent=False, color=BLUE, after=14)
    pdf.paragraph("Origen y Evolución de la Ciencia de Datos", F14B, bold=True, center=True, indent=False, after=35)
    rows = [
        ("Asignatura", "INF-8237 Ciencia de Datos I"),
        ("Participante", "Marlenis Judith Concepción Cuevas"),
        ("Maestro", "Silverio del Orbe"),
        ("Periodo", "17 de mayo al 28 de junio de 2026"),
        ("Horario", "Domingos, 9:00 a.m. a 5:00 p.m."),
        ("Fecha de entrega", "23 de mayo de 2026"),
    ]
    x, y, cw, ch = 290, pdf.y, 560, 82
    for i, (left, right) in enumerate(rows):
        pdf.draw.rectangle([x, y, x + cw, y + ch], fill=LIGHT_BLUE if i % 2 == 0 else LIGHT_GOLD, outline=BLACK)
        pdf.draw.rectangle([x + cw, y, x + (cw * 2), y + ch], fill=GRAY if i % 2 == 0 else "white", outline=BLACK)
        pdf.draw.text((x + 22, y + 22), left, font=F12B, fill=BLUE)
        pdf.draw.text((x + cw + 22, y + 22), right, font=F12, fill=BLACK)
        y += ch
    pdf.y = y + 60
    pdf.paragraph("Santo Domingo, República Dominicana", F12, center=True, indent=False)


def extract_text():
    doc = Document(DOCX)
    items = []
    started = False
    for p in doc.paragraphs:
        text = p.text.strip()
        if text == "Resumen":
            started = True
        if not started or not text or text.startswith("Haga clic derecho"):
            continue
        style = p.style.name if p.style else ""
        items.append((text, style))
    return items


def main():
    pdf = PdfBuilder()
    cover(pdf)
    items = extract_text()
    toc_entries = [
        "Resumen",
        "Abstract",
        "Origen y Evolución de la Ciencia de Datos",
        "Introducción",
        "Marco de referencia",
        "Padre fundador",
        "Primeras revistas y conferencias científicas",
        "Minería de datos versus matemáticas estadísticas",
        "Surgimiento de los algoritmos",
        "Sociedades que lideran este campo",
        "Línea de tiempo",
        "Conclusiones",
        "Referencias",
        "Anexo",
    ]
    prelim = {"Resumen", "Abstract", "Tabla de contenido"}
    current = None
    for text, style in items:
        if text in prelim:
            pdf.new_page("roman" if text == "Resumen" else None)
            current = text
            pdf.heading(text)
            if text == "Tabla de contenido":
                for entry in toc_entries:
                    pdf.paragraph(entry, F12, indent=False, after=8)
            continue
        if text == "Origen y Evolución de la Ciencia de Datos":
            pdf.new_page("arabic")
            current = "body"
            pdf.heading(text)
            continue
        if style.startswith("Heading 1"):
            if text in {"Referencias", "Anexo"}:
                pdf.new_page()
            pdf.heading(text)
        elif style.startswith("Heading 2"):
            pdf.heading(text, level=2)
            if text == "Anexo A. Código QR de la línea de tiempo":
                pass
        elif text == "Figura 1":
            pdf.paragraph(text, F12B, bold=True, indent=False, after=10)
        elif text.startswith("Línea de tiempo resumida"):
            pdf.paragraph(text, F12I, italic=True, indent=False, after=20)
            pdf.image(TIMELINE, W - 2 * M)
        elif text.startswith("El Anexo A presenta"):
            pdf.paragraph(text)
            pdf.image(QR, 320)
        elif text.startswith("Palabras clave") or text.startswith("Keywords") or text.startswith("Nota."):
            pdf.paragraph(text, F12I if not text.startswith("Nota.") else F10, italic=True, indent=False)
        elif current == "Tabla de contenido":
            continue
        elif text.startswith("Enlace del QR"):
            pdf.paragraph(text, F10, indent=False)
        elif current == "body" and text.startswith(("Association for", "Breiman,", "Cleveland,", "Dhar,", "Donoho,", "Fayyad,", "Provost,", "Tukey,")):
            pdf.paragraph(text, F12, indent=False)
        else:
            pdf.paragraph(text, F12, indent=not style.startswith("Heading"))
    pdf.finish()
    print(PDF)


if __name__ == "__main__":
    main()
