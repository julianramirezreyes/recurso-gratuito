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
- After results, a subtle downward cue card invites visitors to continue to the existing ebook CTA. The whole card is the scroll target's clickable/focusable control, without a separate visible button, and scrolls without changing the hash. The existing CTA remains visible on `#guia` and retains the only outbound ebook link to `https://modoverbo.vercel.app/`.
- Respect `prefers-reduced-motion` for the cue animation and smooth scrolling. No purchase language.
- Center the “Ver mis recomendaciones” action beneath its diagnostic callout. When the cue scrolls to the ebook CTA, show the CTA heading and move keyboard focus there without changing the route.
- No remote push, deploy, PR, or merge is authorized for this feature.

## Verification configuration
- Strict TDD: enabled by project instruction. Observe RED → GREEN → REFACTOR for each behavior.
- Test runner: `python3 -m unittest discover -s tests -v`.
- Delivery strategy: `ask-on-risk`; authored-line forecast approximately 350–450 lines across implementation and tests. Treat ~400 lines as a planning heuristic, not a reason to omit tests or compress code.
- Commit each independently useful task with tests and docs in the same Conventional Commit, without AI attribution.

## Tasks
- [x] **T1 — Personalized guide results.** Add the result action and nine signal-matched evidence-informed cards in original order; handle empty and stale selections; keep focus/status accessible. Route: delegated writer, because this requires preparation and non-trivial HTML/CSS/JS plus tests. Acceptance observed: selecting only signals 1, 5, 6 yields only their three cards; no selection and changed selection behave correctly. Checks: focused Node-backed runtime test, full `python3 -m unittest discover -s tests -v` (19 passed), `node --check speaking-recommendations.js`, and `git diff --check` passed. The runtime harness uses a fake DOM; real-browser focus and screen-reader announcements remain unverified. Rollback boundary: the T1 recommendation markup/style/script include in `index.html`, `speaking-recommendations.js`, and `tests/test_speaking_recommendations.py`. Commit: `9b4bc4a` (`feat(guide): show personalized speaking practices`); risk assessment high due test process boundary, RDD globally off, so no native review run.
- [ ] **T2 — Contextual ebook continuation.** Show a subtle downward cue card only after resource 3 results; the entire card is keyboard-operable and scrolls to the existing shared ebook CTA without changing `#guia`, then focuses its heading. No separate visible scroll button. Keep the existing CTA visible on all routes with its outbound link. Center the recommendation action. Route: delegated writer, because route behavior, animation, accessibility, reduced-motion support, and tests are non-trivial. Acceptance observed in code/fake DOM: cue hidden before/stale/empty results; full-card pointer and keyboard activation through a native button overlay, visible focus ring, start-aligned scroll and heading focus, reduced-motion behavior, centered recommendation action, and single outbound link. Checks: focused test 1/1, full `python3 -m unittest discover -s tests -v` 19/19, `node --check speaking-recommendations.js`, and `git diff --check` passed; independent verifier found no substantive issue. Real mobile rendering and assistive-technology behavior remain unverified. Commit: pending while user previews the local design and delivery strategy is unresolved.

## Progress and next step
Design approved by user with “De una”. Branch created from clean `main` at `809c78f`. T1 closed in `9b4bc4a`; authored count so far is 392 additions plus deletions. Independent verifier flagged an inaccurate description of a post-stroke aphasia observational study and source mismatch for repetition; both were corrected before commit. User revised T2 on 2026-09-27 to a scroll cue instead of a duplicate outbound CTA and requested centering the recommendation action; these passed local checks. After browser preview, user approved removing the inner button and making the whole cue card clickable. This latest refinement is implemented and independently verified locally, still uncommitted pending visual feedback. Real-browser/mobile and assistive-technology behavior remains partly unverified because agent file navigation was blocked by the browser policy. The cumulative authored change likely exceeds ~400 lines; delivery strategy remains unresolved, so do not commit T2 or push. No remote work is authorized.
