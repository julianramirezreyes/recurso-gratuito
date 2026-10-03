import unittest
from html.parser import HTMLParser
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "privacidad" / "index.html"


class PolicyParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.scripts = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "script":
            self.scripts.append(attrs)
        if tag == "link":
            self.links.append(attrs)

    def handle_data(self, data):
        self.text.append(data)


class PrivacyPolicyTests(unittest.TestCase):
    def test_public_privacy_route_contains_approved_app_scoped_policy(self):
        self.assertTrue(PAGE.is_file(), "The /privacidad page must exist")
        parser = PolicyParser()
        parser.feed(PAGE.read_text(encoding="utf-8"))
        content = " ".join(" ".join(parser.text).split())

        self.assertIn("Política de privacidad de Oficina de Agentes", content)
        self.assertIn("únicamente a las interacciones con la app Oficina de Agentes", content)
        self.assertIn("@modoverbo", content)
        self.assertIn("modoverbo@gmail.com", content)
        self.assertIn("nombre de usuario de Instagram", content)
        self.assertIn("texto de ese comentario o mensaje", content)
        self.assertIn("No guardamos una copia propia", content)
        self.assertIn("No vendemos ni compartimos con terceros", content)
        self.assertIn("puedes gestionarlo desde Instagram", content)

    def test_privacy_page_has_no_scripts_or_external_assets(self):
        self.assertTrue(PAGE.is_file(), "The /privacidad page must exist")
        parser = PolicyParser()
        parser.feed(PAGE.read_text(encoding="utf-8"))

        self.assertEqual([], parser.scripts)
        self.assertFalse(any(link.get("href", "").startswith("http") for link in parser.links))


if __name__ == "__main__":
    unittest.main()
