import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "index.html"


class FeaturedResourceParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.section_order = []
        self.resource_ids = set()
        self.in_feature = False
        self.in_heading = False
        self.in_copy = False
        self.in_link = False
        self.heading_parts = []
        self.copy_parts = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if attrs.get("id"):
            self.resource_ids.add(attrs["id"])
        if tag == "section":
            self.section_order.append(next(
                (name for name in ("home-hero", "featured-resource", "home-resources") if name in classes),
                "other",
            ))
        if tag == "section" and "featured-resource" in classes:
            self.in_feature = True
        if not self.in_feature:
            return
        if tag == "h2":
            self.in_heading = True
        elif tag == "p" and "featured-resource__description" in classes:
            self.in_copy = True
        elif tag == "a":
            self.in_link = True
            self.links.append({"href": attrs.get("href"), "text": []})

    def handle_endtag(self, tag):
        if tag == "h2":
            self.in_heading = False
        elif tag == "p" and self.in_copy:
            self.in_copy = False
        elif tag == "a" and self.in_link:
            self.in_link = False
        elif tag == "section" and self.in_feature:
            self.in_feature = False

    def handle_data(self, data):
        if self.in_heading:
            self.heading_parts.append(data.strip())
        if self.in_copy:
            self.copy_parts.append(data.strip())
        if self.in_link and self.links:
            self.links[-1]["text"].append(data.strip())


class FeaturedResourceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.page = FeaturedResourceParser()
        cls.page.feed(cls.html)

    def test_featured_resource_sits_between_home_hero_and_catalog(self):
        self.assertLess(self.page.section_order.index("home-hero"), self.page.section_order.index("featured-resource"))
        self.assertLess(self.page.section_order.index("featured-resource"), self.page.section_order.index("home-resources"))

    def test_featured_resource_names_the_current_guide_and_links_to_its_route(self):
        self.assertEqual("Cómo mejorar tu forma de hablar", " ".join(self.page.heading_parts))
        self.assertIn("guia", self.page.resource_ids)
        self.assertEqual(1, len(self.page.links))
        self.assertEqual("#guia", self.page.links[0]["href"])
        self.assertTrue(self.page.links[0]["text"])

    def test_featured_copy_describes_a_diagnostic_without_claiming_a_finished_guide(self):
        description = " ".join(self.page.copy_parts).casefold()
        self.assertRegex(description, re.compile(r"diagn[oó]stic"))
        self.assertRegex(description, re.compile(r"gu[ií]a completa"))
        self.assertRegex(description, re.compile(r"a[uú]n|todav[ií]a"))
        self.assertRegex(description, re.compile(r"preparaci[oó]n|incompleta|por completar"))


if __name__ == "__main__":
    unittest.main()
