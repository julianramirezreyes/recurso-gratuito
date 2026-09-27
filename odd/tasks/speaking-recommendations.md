# Speaking recommendations and ebook continuation

## Objective
Turn resource 3's nine-signal checklist into a useful, personalized practice result, then offer a contextual path to the ebook without sales language.

## Problem and rationale
The current checklist ends with static instructions and gives no tailored next step. The user approved a button that reveals only recommendations matching checked signals, followed by an ebook CTA.

## Scope and constraints
- Work only on the existing static site and its tests, on `feat/speaking-recommendations`.
- Preserve the nine existing signal labels and their order. Multi-select stays enabled.
- Each revealed card has a practical short exercise, something observable, a source link, and any relevant non-clinical caveat.
- No selections must yield a clear inline prompt. Changed selections must invalidate old results until the button is pressed again.
- Results and contextual CTA appear only after the action; do not persist answers.
- The contextual ebook link is `https://modoverbo.vercel.app/`, with no purchase language. Hide the shared ebook aside on `#guia` only; retain it elsewhere.
- No remote push, deploy, PR, or merge is authorized for this feature.

## Verification configuration
- Strict TDD: enabled by project instruction. Observe RED → GREEN → REFACTOR for each behavior.
- Test runner: `python3 -m unittest discover -s tests -v`.
- Delivery strategy: `ask-on-risk`; authored-line forecast approximately 350–450 lines across implementation and tests. Treat ~400 lines as a planning heuristic, not a reason to omit tests or compress code.
- Commit each independently useful task with tests and docs in the same Conventional Commit, without AI attribution.

## Tasks
- [ ] **T1 — Personalized guide results.** Add the result action and nine signal-matched evidence-informed cards in original order; handle empty and stale selections; keep focus/status accessible. Route: delegated writer, because this requires preparation and non-trivial HTML/CSS/JS plus tests. Acceptance: selecting only signals 1, 5, 6 yields only their three cards; no selection and changed selection behave correctly. Checks: focused recommendation tests and full unittest suite. Commit: pending.
- [ ] **T2 — Contextual ebook continuation.** Show a non-sales CTA only after resource 3 results and suppress the shared ebook aside only on `#guia`. Route: delegated writer, because route behavior plus tests is non-trivial. Acceptance: correct link and copy; no duplicate on `#guia`; shared CTA unchanged on other routes; hidden before results. Checks: focused CTA tests and full unittest suite. Commit: pending.

## Progress and next step
Design approved by user with “De una”. Branch created from clean `main` at `809c78f`. No source changes yet. Implement T1 with RED before code.
