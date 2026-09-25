import hashlib
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LANDING_URL = "https://modoverbo.vercel.app/"
COVER_PATH = "assets/ebook/cover.webp"


class EbookCardParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_card = False
        self.in_title = False
        self.in_description = False
        self.title_parts = []
        self.description_parts = []
        self.links = []
        self.images = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "aside" and "ebook-cta" in classes:
            self.in_card = True
            return
        if not self.in_card:
            return
        if tag == "h2":
            self.in_title = True
        if tag == "p" and "tag" not in classes:
            self.in_description = True
        if tag == "a":
            self.links.append(attrs.get("href"))
        if tag == "img":
            self.images.append((attrs.get("src"), attrs.get("alt")))

    def handle_endtag(self, tag):
        if tag == "aside" and self.in_card:
            self.in_card = False
            return
        if not self.in_card:
            return
        if tag == "h2":
            self.in_title = False
        if tag == "p" and self.in_description:
            self.in_description = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data.strip())
        if self.in_description:
            self.description_parts.append(data.strip())


class EbookPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.card = EbookCardParser()
        cls.card.feed(cls.html)

    def test_promotion_matches_the_landing_message(self):
        title = " ".join(part for part in self.card.title_parts if part)
        description = " ".join(part for part in self.card.description_parts if part)
        self.assertEqual("Haz que tus ideas lleguen con claridad.", title)
        self.assertEqual(
            "Historias, ejemplos y ejercicios para ordenar lo que piensas y expresarlo en conversaciones reales.",
            description,
        )

    def test_ebook_cta_keeps_the_confirmed_destination(self):
        self.assertIn(LANDING_URL, self.card.links)

    def test_promotion_uses_one_flat_local_cover(self):
        image_path = ROOT / COVER_PATH
        self.assertTrue(image_path.is_file())
        image = image_path.read_bytes()
        versioned_path = f"{COVER_PATH}?v={hashlib.sha256(image).hexdigest()[:8]}"
        self.assertEqual([(versioned_path, "Portada del ebook Elocuencia sin miedo")], self.card.images)
        self.assertGreater(len(image), 12)
        self.assertEqual(b"RIFF", image[:4])
        self.assertEqual(b"WEBP", image[8:12])


if __name__ == "__main__":
    unittest.main()
