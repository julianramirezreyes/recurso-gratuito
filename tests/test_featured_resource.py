import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "index.html"


def css_block_at(css, start):
    opening = css.find("{", start)
    if opening == -1:
        return None
    depth = 0
    for index in range(opening, len(css)):
        if css[index] == "{":
            depth += 1
        elif css[index] == "}":
            depth -= 1
            if depth == 0:
                return css[opening + 1:index]
    return None


def css_block(css, selector):
    match = re.search(re.escape(selector) + r"\s*\{", css)
    if not match:
        return None
    return css_block_at(css, match.start())


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
        self.in_style = False
        self.styles = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "style":
            self.in_style = True
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
        if tag == "style":
            self.in_style = False
        elif tag == "h2":
            self.in_heading = False
        elif tag == "p" and self.in_copy:
            self.in_copy = False
        elif tag == "a" and self.in_link:
            self.in_link = False
        elif tag == "section" and self.in_feature:
            self.in_feature = False

    def handle_data(self, data):
        if self.in_style:
            self.styles.append(data)
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

    def test_featured_border_glow_is_slow_and_disabled_for_reduced_motion(self):
        css = "\n".join(self.page.styles)
        card_rule = css_block(css, ".featured-resource")
        animation = re.search(
            r"animation:\s*([\w-]+)\s+([\d.]+)s\s+ease-in-out\s+infinite\b",
            card_rule or "",
        )
        self.assertIsNotNone(animation, "The featured card should animate its glow slowly and continuously")
        self.assertGreaterEqual(float(animation.group(2)), 6)

        keyframes = css_block(css, "@keyframes " + animation.group(1))
        self.assertIsNotNone(keyframes)
        self.assertIn("box-shadow:", keyframes)
        self.assertNotRegex(keyframes, r"\b(?:transform|opacity|width|height|padding|border-width)\s*:")
        self.assertNotRegex(
            css_block(css, ".featured-resource__cta") or "",
            r"\banimation\s*:",
        )

        reduced_motion = re.search(
            r"@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)\s*\{",
            css,
        )
        self.assertIsNotNone(reduced_motion, "Reduced-motion users need a static featured-card treatment")
        reduced_block = css_block_at(css, reduced_motion.start())
        reduced_card = css_block(reduced_block or "", ".featured-resource")
        self.assertIsNotNone(reduced_card)
        self.assertRegex(reduced_card, r"animation\s*:\s*none\b")
        self.assertRegex(reduced_card, r"box-shadow\s*:\s*[^;]+rgba\(")

    def test_featured_sheen_is_layered_over_card_background_and_under_content(self):
        css = "\n".join(self.page.styles)
        card_rule = css_block(css, ".featured-resource") or ""
        sheen_rule = css_block(css, ".featured-resource::before")
        copy_rule = css_block(css, ".featured-resource__copy") or ""
        cta_rule = css_block(css, ".featured-resource__cta") or ""

        self.assertRegex(card_rule, r"overflow\s*:\s*hidden\b")
        self.assertIsNotNone(sheen_rule, "The featured card needs a dedicated sheen layer")
        self.assertRegex(sheen_rule or "", r"position\s*:\s*absolute\b")
        self.assertRegex(sheen_rule or "", r"pointer-events\s*:\s*none\b")
        self.assertRegex(sheen_rule or "", r"z-index\s*:\s*0\b")
        self.assertRegex(sheen_rule or "", r"linear-gradient\([^;]*transparent[^;]*rgba\(")
        sweep = re.search(
            r"animation\s*:\s*featured-resource-sheen\s+([\d.]+)s\b",
            sheen_rule or "",
        )
        self.assertIsNotNone(sweep)
        self.assertGreaterEqual(float(sweep.group(1)), 6)
        band_width = re.search(r"width\s*:\s*([\d.]+)%", sheen_rule or "")
        self.assertIsNotNone(band_width)
        self.assertLess(float(band_width.group(1)), 40)
        self.assertRegex(copy_rule, r"position\s*:\s*relative\b")
        self.assertRegex(copy_rule, r"z-index\s*:\s*1\b")
        self.assertRegex(cta_rule, r"position\s*:\s*relative\b")
        self.assertRegex(cta_rule, r"z-index\s*:\s*1\b")

        keyframes = css_block(css, "@keyframes featured-resource-sheen") or ""
        self.assertRegex(keyframes, r"transform\s*:\s*translateX\(")
        self.assertIn("opacity:", keyframes)
        self.assertNotRegex(keyframes, r"\b(?:width|height|padding|border-width)\s*:")

        reduced_motion = re.search(
            r"@media\s*\(\s*prefers-reduced-motion\s*:\s*reduce\s*\)\s*\{",
            css,
        )
        self.assertIsNotNone(reduced_motion)
        reduced_block = css_block_at(css, reduced_motion.start()) if reduced_motion else ""
        reduced_sheen = css_block(reduced_block or "", ".featured-resource::before")
        self.assertIsNotNone(reduced_sheen)
        self.assertRegex(reduced_sheen or "", r"animation\s*:\s*none\b")


if __name__ == "__main__":
    unittest.main()
