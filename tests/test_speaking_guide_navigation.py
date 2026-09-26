import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "index.html"


class SpeakingGuideParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resource_ids = set()
        self.fragments = []
        self.home_cards = []
        self.in_home_grid = False
        self.current_card = None
        self.current_heading = False
        self.current_paragraph = False
        self.current_signal = False
        self.current_prompt = False
        self.guide_heading = []
        self.guide_intro = []
        self.diagnostic_heading = []
        self.prompts = []
        self.signals = []
        self.in_guide = False
        self.in_diagnostic = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if "id" in attrs:
            self.resource_ids.add(attrs["id"])
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.fragments.append(attrs["href"][1:])
        if tag == "div" and "home-grid" in classes:
            self.in_home_grid = True
        if self.in_home_grid and tag in {"a", "article"} and "home-card" in classes:
            self.current_card = {"href": attrs.get("href"), "text": []}
        if tag == "div" and attrs.get("id") == "guia":
            self.in_guide = True
        if tag == "section" and attrs.get("id") == "diagnostico":
            self.in_diagnostic = True
        if self.in_guide and tag == "h1":
            self.current_heading = True
        if self.in_guide and tag == "p" and "guide-intro" in classes:
            self.current_paragraph = True
        if self.in_diagnostic and tag == "li" and "prompt" in classes:
            self.current_signal = False
            self.prompts.append([])
            self.current_prompt = True
        elif self.in_diagnostic and tag == "label" and "signal" in classes:
            self.current_signal = True
            self.current_prompt = False
            self.signals.append([])

    def handle_endtag(self, tag):
        if tag == "h1":
            self.current_heading = False
        if tag == "p" and self.current_paragraph:
            self.current_paragraph = False
        if tag == "li":
            self.current_prompt = False
        if tag == "label":
            self.current_signal = False
        if tag == "div" and self.in_home_grid:
            self.in_home_grid = False
        if tag == "div" and self.in_guide:
            self.in_guide = False
        if tag == "section" and self.in_diagnostic:
            self.in_diagnostic = False
        if tag in {"a", "article"} and self.current_card is not None:
            self.home_cards.append(self.current_card)
            self.current_card = None

    def handle_data(self, data):
        value = data.strip()
        if not value:
            return
        if self.current_card is not None:
            self.current_card["text"].append(value)
        if self.current_heading:
            self.guide_heading.append(value)
        if self.current_paragraph:
            self.guide_intro.append(value)
        if self.current_prompt:
            self.prompts[-1].append(value)
        if self.current_signal:
            self.signals[-1].append(value)


class SpeakingGuideNavigationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.page = SpeakingGuideParser()
        cls.page.feed(cls.html)

    def test_home_cards_link_to_guide_and_move_unavailable_card_to_slot_four(self):
        cards = self.page.home_cards
        self.assertEqual(["#trabalenguas", "#frases", "#guia"], [card["href"] for card in cards[:3]])
        self.assertIn("Cómo mejorar tu forma de hablar", " ".join(cards[2]["text"]))
        self.assertIn("04 · En camino", " ".join(cards[3]["text"]))
        self.assertIn("Aún no disponible", " ".join(cards[3]["text"]))
        self.assertEqual(4, len(cards))

    def test_guide_route_has_a_practical_intro_and_four_diagnostic_prompts(self):
        self.assertIn("guia", self.page.resource_ids)
        self.assertIn("guia", self.page.fragments)
        self.assertEqual(["Cómo mejorar tu forma de hablar"], self.page.guide_heading)
        self.assertIn("Hablar mejor no significa hablar complicado", " ".join(self.page.guide_intro))
        self.assertEqual(4, len(self.page.prompts))
        self.assertGreaterEqual(len(self.page.signals), 6)

    def test_guide_route_has_its_own_document_title(self):
        self.assertRegex(
            self.html,
            re.compile(r"guia:'Cómo mejorar tu forma de hablar'"),
        )


if __name__ == "__main__":
    unittest.main()
