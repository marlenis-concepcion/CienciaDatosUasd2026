from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "index.html"


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
    assert "Documents/NETWORKING" not in text
