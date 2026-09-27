import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.fragments = []
        self.header_depth = 0
        self.header_text = []
        self.home_eyebrow = []
        self.in_home_eyebrow = False
        self.home_eyebrow_found = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.fragments.append(attrs["href"][1:])
        if tag == "header":
            self.header_depth += 1
        if (
            tag == "p"
            and "eyebrow" in attrs.get("class", "").split()
            and not self.home_eyebrow_found
        ):
            self.in_home_eyebrow = True

    def handle_endtag(self, tag):
        if tag == "header" and self.header_depth:
            self.header_depth -= 1
        if tag == "p" and self.in_home_eyebrow:
            self.in_home_eyebrow = False
            self.home_eyebrow_found = True

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.header_depth:
            self.header_text.append(text)
        if self.in_home_eyebrow:
            self.home_eyebrow.append(text)


class HomeCatalogParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.current = None
        self.depth = 0
        self.capture_heading = False
        self.capture_status = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if self.current is None and tag in {"a", "article"} and "home-card" in classes:
            self.current = {
                "tag": tag,
                "href": attrs.get("href"),
                "classes": classes,
                "number": None,
                "heading": [],
                "status": [],
            }
            self.depth = 1
            return
        if self.current is None:
            return
        self.depth += 1
        if tag == "h3":
            self.capture_heading = True
        if "home-soon-label" in classes:
            self.capture_status = True
        if "tag" in classes and self.current["number"] is None:
            self.current["number"] = True

    def handle_endtag(self, tag):
        if self.current is None:
            return
        if tag == "h3":
            self.capture_heading = False
        if self.capture_status and tag == "span":
            self.capture_status = False
        self.depth -= 1
        if self.depth == 0:
            self.cards.append(self.current)
            self.current = None

    def handle_data(self, data):
        if self.current is None:
            return
        text = data.strip()
        if not text:
            return
        if self.capture_heading:
            self.current["heading"].append(text)
        if self.capture_status:
            self.current["status"].append(text)
        if self.current["number"] is True:
            match = re.match(r"(\d{2})\s*·", text)
            if match:
                self.current["number"] = match.group(1)


class HomeNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.page = PageParser()
        cls.page.feed(cls.html)

    def test_header_and_home_eyebrow_use_neutral_branding(self):
        self.assertEqual(["∿", "MODO VERBO"], self.page.header_text)
        self.assertEqual(["Modo Verbo · Practica a tu ritmo"], self.page.home_eyebrow)
        self.assertNotIn("Recursos gratuitos", " ".join(self.page.header_text + self.page.home_eyebrow))
        self.assertNotIn('id="resourceHeader"', self.html)
        self.assertNotIn("resourceHeader", self.html)

    def test_hash_navigation_targets_existing_resource_pages(self):
        route_ids = {"inicio", "trabalenguas", "frases"}
        self.assertTrue(route_ids.issubset(self.page.ids))
        self.assertTrue(route_ids.issubset(set(self.page.fragments)))

    def test_home_catalog_keeps_numbered_order_routes_and_non_clickable_coming_soon_item(self):
        catalog = HomeCatalogParser()
        catalog.feed(self.html)

        self.assertEqual(
            ["01", "02", "03", "04"],
            [card["number"] for card in catalog.cards],
        )
        self.assertEqual(
            ["#trabalenguas", "#frases", "#guia", None],
            [card["href"] for card in catalog.cards],
        )
        self.assertEqual("article", catalog.cards[3]["tag"])
        self.assertIn("home-card--soon", catalog.cards[3]["classes"])
        self.assertIn("Aún no disponible", " ".join(catalog.cards[3]["status"]))

    def test_route_specific_document_titles_remain_unchanged(self):
        self.assertRegex(
            self.html,
            re.compile(
                r"const names=\{inicio:'Recursos para hablar mejor',"
                r"trabalenguas:'Biblioteca de trabalenguas',"
                r"frases:'Frases para hablar mejor',"
            ),
        )


if __name__ == "__main__":
    unittest.main()
