from html.parser import HTMLParser
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"
ARTICLE = ROOT / "docs" / "Articulo_Cientifico_OULAD_APA7.docx"


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "img" and "src" in attributes:
            self.images.append(attributes["src"])


def test_html_documentation_has_required_sections():
    text = HTML.read_text(encoding="utf-8")
    for section_id in [
        "resumen",
        "hipotesis",
        "osemn",
        "arquitectura",
        "resultados",
        "pruebas",
        "entregables",
    ]:
        assert f'id="{section_id}"' in text


def test_local_html_links_and_images_resolve():
    parser = LinkCollector()
    parser.feed(HTML.read_text(encoding="utf-8"))
    local_targets = [
        target
        for target in parser.links + parser.images
        if not target.startswith(("#", "http://", "https://", "mailto:"))
    ]
    assert local_targets
    assert all((ROOT / target).exists() for target in local_targets)


def test_html_contains_no_personal_absolute_path():
    text = HTML.read_text(encoding="utf-8")
    assert "/Users/" not in text
    assert "Documents" + "/NETWORKING" not in text


def test_article_uses_apa_paragraph_formatting():
    document = Document(ARTICLE)
    paragraphs = document.paragraphs

    cover_end = next(
        index for index, paragraph in enumerate(paragraphs)
        if paragraph.text.startswith("Fecha:")
    )
    cover = [paragraph for paragraph in paragraphs[:cover_end + 1] if paragraph.text]
    assert all(paragraph.alignment == WD_ALIGN_PARAGRAPH.CENTER for paragraph in cover)
    assert any(paragraph.text == "Equipo: McCarthy Team" for paragraph in cover)
    assert any(
        paragraph.text == "Facilitador: Dr. Silverio del Orbe Abad"
        for paragraph in cover
    )

    summary_heading = next(
        index for index, paragraph in enumerate(paragraphs)
        if paragraph.text == "Resumen" and paragraph.style.name == "Heading 1"
    )
    summary = paragraphs[summary_heading + 1]
    assert summary.alignment == WD_ALIGN_PARAGRAPH.LEFT
    assert summary.paragraph_format.line_spacing == 2
    assert summary.paragraph_format.first_line_indent == Inches(0)

    introduction_heading = next(
        index for index, paragraph in enumerate(paragraphs)
        if paragraph.text == "Introducción" and paragraph.style.name == "Heading 1"
    )
    introduction = paragraphs[introduction_heading + 1]
    assert introduction.alignment == WD_ALIGN_PARAGRAPH.LEFT
    assert introduction.paragraph_format.line_spacing == 2
    assert introduction.paragraph_format.first_line_indent == Inches(0.5)

    references_heading = next(
        index for index, paragraph in enumerate(paragraphs)
        if paragraph.text == "Referencias" and paragraph.style.name == "Heading 1"
    )
    reference = paragraphs[references_heading + 1]
    assert reference.paragraph_format.left_indent == Inches(0.5)
    assert reference.paragraph_format.first_line_indent == Inches(-0.5)
