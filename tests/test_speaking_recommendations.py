import re
import subprocess
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "index.html"
SCRIPT = ROOT / "speaking-recommendations.js"


RUNTIME_SCENARIO = r"""
const assert = require('node:assert/strict');
const { init } = require(process.argv[1]);

class Element {
  constructor() {
    this.hidden = false;
    this.innerHTML = '';
    this.textContent = '';
    this.listeners = {};
    this.focused = false;
    this.focusCalls = [];
    this.scrollCalls = [];
  }
  addEventListener(name, listener) { this.listeners[name] = listener; }
  focus(options) { this.focused = true; this.focusCalls.push(options); }
  scrollIntoView(options) { this.scrollCalls.push(options); }
  fire(name) { this.listeners[name]?.({ target: this }); }
}

const checkboxes = Array.from({ length: 9 }, () => ({
  checked: false,
  listeners: {},
  addEventListener(name, listener) { this.listeners[name] = listener; },
  fire(name) { this.listeners[name]?.({ target: this }); },
}));
const elements = {
  showRecommendations: new Element(),
  recommendationResults: new Element(),
  recommendationHeading: new Element(),
  recommendationCards: new Element(),
  recommendationStatus: new Element(),
  contextualEbookCue: new Element(),
  sharedEbookCta: new Element(),
  'ebook-cta-title': new Element(),
  scrollToSharedEbookCta: new Element(),
};
elements.recommendationResults.hidden = true;
elements.contextualEbookCue.hidden = true;
const fakeWindow = {
  location: { hash: '#inicio' },
  listeners: {},
  reducedMotion: false,
  matchMedia(query) {
    assert.equal(query, '(prefers-reduced-motion: reduce)');
    return { matches: this.reducedMotion };
  },
  addEventListener(name, listener) { this.listeners[name] = listener; },
  fire(name) { this.listeners[name]?.(); },
};
const fakeDocument = {
  getElementById(id) { return elements[id]; },
  querySelectorAll(selector) {
    assert.equal(selector, '#diagnostico .diagnostic-signals input[type="checkbox"]');
    return checkboxes;
  },
};

init(fakeDocument, fakeWindow);
assert.equal(elements.recommendationResults.hidden, true, 'results start hidden');
assert.equal(elements.recommendationCards.innerHTML, '', 'there are no pre-rendered answers');
assert.equal(elements.contextualEbookCue.hidden, true, 'the contextual cue starts hidden');
assert.equal(elements.sharedEbookCta.hidden, false, 'the shared CTA remains on the home route');

checkboxes[0].checked = true;
checkboxes[4].checked = true;
checkboxes[5].checked = true;
elements.showRecommendations.fire('click');
const cardTitles = [...elements.recommendationCards.innerHTML.matchAll(/<h3>(.*?)<\/h3>/g)].map((match) => match[1]);
assert.deepEqual(cardTitles, [
  'Me quedo en blanco.',
  'Uso muchas muletillas.',
  'No encuentro la palabra exacta.',
], 'only selected signals render, in their original order');
assert.equal((elements.recommendationCards.innerHTML.match(/class="recommendation-source"/g) || []).length, 3, 'every card links a source');
assert.equal((elements.recommendationCards.innerHTML.match(/Práctica de 3–5 minutos/g) || []).length, 3, 'every card has a 3–5 minute exercise');
assert.equal((elements.recommendationCards.innerHTML.match(/3–5 minutos/g) || []).length, 3, 'each card states the duration only once');
assert.equal(elements.recommendationResults.hidden, false);
assert.equal(elements.contextualEbookCue.hidden, false, 'the contextual cue appears with results');
assert.match(elements.recommendationStatus.textContent, /3 recomendaciones/);
assert.equal(elements.recommendationHeading.focused, true, 'focus moves to the result heading');
elements.scrollToSharedEbookCta.fire('click');
assert.deepEqual(elements.sharedEbookCta.scrollCalls.at(-1), { behavior: 'smooth', block: 'start' });
assert.deepEqual(elements['ebook-cta-title'].focusCalls.at(-1), { preventScroll: true }, 'the ebook heading receives focus without overriding the chosen scroll position');
assert.equal(fakeWindow.location.hash, '#inicio', 'scrolling does not change the route hash');
fakeWindow.location.hash = '#guia';
fakeWindow.reducedMotion = true;
elements.scrollToSharedEbookCta.fire('click');
assert.deepEqual(elements.sharedEbookCta.scrollCalls.at(-1), { behavior: 'instant', block: 'start' });
assert.deepEqual(elements['ebook-cta-title'].focusCalls.at(-1), { preventScroll: true });
assert.equal(fakeWindow.location.hash, '#guia', 'reduced-motion scrolling preserves the guide hash');

checkboxes[1].checked = true;
checkboxes[1].fire('change');
assert.equal(elements.recommendationResults.hidden, true, 'changed selection hides stale cards');
assert.equal(elements.contextualEbookCue.hidden, true, 'changed selection also hides the cue');
assert.equal(elements.recommendationCards.innerHTML, '', 'stale card content is removed');
elements.showRecommendations.fire('click');
const refreshedTitles = [...elements.recommendationCards.innerHTML.matchAll(/<h3>(.*?)<\/h3>/g)].map((match) => match[1]);
assert.deepEqual(refreshedTitles, [
  'Me quedo en blanco.',
  'Repito mucho las mismas palabras.',
  'Uso muchas muletillas.',
  'No encuentro la palabra exacta.',
]);

checkboxes.forEach((checkbox) => { checkbox.checked = false; });
elements.showRecommendations.fire('click');
assert.equal(elements.recommendationResults.hidden, true, 'empty selection does not show cards');
assert.equal(elements.contextualEbookCue.hidden, true, 'empty selection keeps the cue hidden');
assert.equal(elements.recommendationCards.innerHTML, '');
assert.match(elements.recommendationStatus.textContent, /Marca al menos una señal/);

checkboxes.forEach((checkbox) => { checkbox.checked = true; });
elements.showRecommendations.fire('click');
const allTitles = [...elements.recommendationCards.innerHTML.matchAll(/<h3>(.*?)<\/h3>/g)].map((match) => match[1]);
assert.deepEqual(allTitles, [
  'Me quedo en blanco.',
  'Repito mucho las mismas palabras.',
  'Hablo demasiado rápido.',
  'Termino las frases sin fuerza.',
  'Uso muchas muletillas.',
  'No encuentro la palabra exacta.',
  'Me cuesta explicar mis ideas.',
  'Mi voz tiembla o pierde volumen.',
  'Me cuesta hablar frente a otras personas.',
], 'all nine cards follow the checklist order');
assert.equal((elements.recommendationCards.innerHTML.match(/class="recommendation-source"/g) || []).length, 9);
assert.equal((elements.recommendationCards.innerHTML.match(/Práctica de 3–5 minutos/g) || []).length, 9);
assert.equal(elements.contextualEbookCue.hidden, false);
fakeWindow.location.hash = '#guia';
fakeWindow.fire('hashchange');
assert.equal(elements.sharedEbookCta.hidden, false, 'the shared CTA remains visible on the guide route');
fakeWindow.location.hash = '#frases';
fakeWindow.fire('hashchange');
assert.equal(elements.sharedEbookCta.hidden, false, 'the shared CTA returns on other routes');
"""


class SpeakingRecommendationsTests(unittest.TestCase):
    def test_browser_runtime_renders_only_checked_cards_and_invalidates_stale_results(self):
        html = PAGE.read_text(encoding="utf-8")
        script = SCRIPT.read_text(encoding="utf-8")
        style_block = html.split("</style>", maxsplit=1)[0]
        self.assertIn('id="showRecommendations"', html, "the guide needs an action to request recommendations")
        self.assertIn('src="speaking-recommendations.js"', html, "the guide needs the tested recommendation behavior")
        self.assertIn("pulsa «Ver mis recomendaciones»", html, "the diagnostic instructions should point to the next action")
        self.assertIn("mitcommlab.mit.edu/be/commkit/public-speaking-how-to-practice/", script)
        self.assertIn("adaptación de autoobservación", script)
        self.assertNotIn("Stanford Oral Communication Program · Delivery", script[script.index("title: 'Repito mucho las mismas palabras.'"):script.index("title: 'Hablo demasiado rápido.'")])
        self.assertIn("estudio observacional", script)
        self.assertIn("43 personas con afasia postictus", script)
        self.assertIn("no evalúa una intervención ni establece eficacia clínica", script)
        self.assertIn("https://pmc.ncbi.nlm.nih.gov/articles/PMC10977788/", script)
        self.assertIn('id="contextualEbookCue"', html)
        self.assertIn('id="scrollToSharedEbookCta"', html)
        self.assertNotIn('type="button">Ver el ebook</button>', html)
        self.assertRegex(
            html,
            re.compile(r'<button class="ebook-cue-link" id="scrollToSharedEbookCta" type="button" aria-label="Bajar al ebook Elocuencia sin miedo"></button>'),
        )
        self.assertIn('Desliza un poco más para descubrir Elocuencia sin miedo', html)
        self.assertEqual(1, html.count('href="https://modoverbo.vercel.app/"'))
        self.assertRegex(html, re.compile(r'<aside class="ebook-cta" id="sharedEbookCta"[^>]*>'))
        self.assertRegex(html, re.compile(r'\.recommendation-action\s*\{[^}]*display:\s*block;[^}]*margin-inline:\s*auto;', re.DOTALL))
        self.assertRegex(html, re.compile(r'<h2 id="ebook-cta-title"[^>]*tabindex="-1"'))
        self.assertRegex(style_block, re.compile(r"\.contextual-ebook-cue\[hidden\]\s*\{[^}]*display:\s*none\s*!important;"))
        self.assertRegex(style_block, re.compile(r"\.contextual-ebook-cue\s*\{[^}]*position:\s*relative;[^}]*cursor:\s*pointer;", re.DOTALL))
        self.assertRegex(style_block, re.compile(r"\.ebook-cue-link\s*\{[^}]*position:\s*absolute;[^}]*inset:\s*0;[^}]*opacity:\s*0;", re.DOTALL))
        self.assertRegex(style_block, re.compile(r"\.contextual-ebook-cue:focus-within\s*\{[^}]*outline:", re.DOTALL))
        self.assertIn("@media (prefers-reduced-motion: reduce)", style_block)
        self.assertRegex(style_block, re.compile(r"\.ebook-cue-arrows\s*\{[^}]*animation:\s*none;"))
        self.assertRegex(style_block, re.compile(r"#recommendationCards\s*\{[^}]*display:\s*grid;[^}]*gap:\s*"))
        self.assertRegex(
            html,
            re.compile(r'id="recommendationHeading"[^>]*>.*?</h2>\s*<p class="recommendation-note">.*?adaptaciones prácticas.*?no son protocolos clínicamente validados.*?</p>\s*<div id="recommendationCards"', re.DOTALL),
        )
        result = subprocess.run(
            ["node", "-e", RUNTIME_SCENARIO, str(SCRIPT)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
