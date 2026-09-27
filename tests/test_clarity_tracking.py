import json
import subprocess
import unittest
from html.parser import HTMLParser
from pathlib import Path


PAGE = Path(__file__).resolve().parents[1] / "index.html"


class HeadScriptParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.in_script = False
        self.scripts = []

    def handle_starttag(self, tag, attrs):
        if tag == "head":
            self.in_head = True
        elif tag == "script" and self.in_head:
            self.in_script = True
            self.scripts.append("")

    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False
        elif tag == "head":
            self.in_head = False

    def handle_data(self, data):
        if self.in_script:
            self.scripts[-1] += data


class ClarityTrackingTests(unittest.TestCase):
    def test_tracking_script_loads_correct_project_from_head(self):
        parser = HeadScriptParser()
        parser.feed(PAGE.read_text(encoding="utf-8"))
        scripts = [script for script in parser.scripts if "clarity.ms" in script]
        self.assertEqual(1, len(scripts))

        harness = """
            const vm = require('node:vm');
            const fs = require('node:fs');
            const inserted = [];
            const first = { parentNode: { insertBefore(node) { inserted.push(node); } } };
            const document = {
              createElement(tag) { return { tag }; },
              getElementsByTagName() { return [first]; },
            };
            const window = {};
            vm.runInNewContext(fs.readFileSync(0, 'utf8'), { window, document });
            window.clarity('event', 'test');
            process.stdout.write(JSON.stringify({
              scripts: inserted.map(({ src, async }) => ({ src, async })),
              queued: window.clarity.q.map(args => Array.from(args)),
            }));
        """
        result = subprocess.run(
            ["node", "-e", harness], input=scripts[0], text=True,
            capture_output=True, check=True,
        )
        self.assertEqual(
            [{"src": "https://www.clarity.ms/tag/yp0zlnbypw", "async": 1}],
            json.loads(result.stdout)["scripts"],
        )
        self.assertEqual([["event", "test"]], json.loads(result.stdout)["queued"])


if __name__ == "__main__":
    unittest.main()
