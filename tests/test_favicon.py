import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"
FAVICON = ROOT / "assets" / "favicon.svg"


class IconLinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.icons = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and "icon" in attrs.get("rel", "").split():
            self.icons.append(attrs)


class FaviconTests(unittest.TestCase):
    def test_page_links_to_local_svg_favicon(self):
        parser = IconLinkParser()
        parser.feed(PAGE.read_text(encoding="utf-8"))

        self.assertEqual(1, len(parser.icons))
        self.assertEqual("image/svg+xml", parser.icons[0].get("type"))
        self.assertEqual("assets/favicon.svg", parser.icons[0].get("href"))
        self.assertTrue(FAVICON.is_file())

    def test_favicon_is_self_contained_brand_colored_square_svg(self):
        svg = ET.parse(FAVICON).getroot()

        self.assertEqual("svg", svg.tag.rsplit("}", 1)[-1])
        self.assertEqual("0 0 64 64", svg.get("viewBox"))
        elements = list(svg.iter())
        self.assertFalse(any(element.tag.rsplit("}", 1)[-1] == "text" for element in elements))
        self.assertFalse(any("href" in element.attrib for element in elements))
        self.assertFalse(any("url(" in value for element in elements for value in element.attrib.values()))

        fills_and_strokes = {
            value.lower()
            for element in elements
            for key, value in element.attrib.items()
            if key in {"fill", "stroke"}
        }
        self.assertIn("#111110", fills_and_strokes)
        self.assertIn("#fa5a25", fills_and_strokes)


if __name__ == "__main__":
    unittest.main()
