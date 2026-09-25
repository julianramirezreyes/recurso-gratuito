# Refresh the ebook CTA

## Objective

Remove the outdated "Recursos gratuitos" branding and align the ebook promotion with the current *Elocuencia sin miedo* cover and landing. Visitors should still reach the user-confirmed landing at `https://modoverbo.vercel.app/`.

## Scope and constraints

- Edit this repository only; read the sibling ebook and landing projects as visual references.
- Do not change the ebook landing URL, purchase checkout, or the existing Netlify redirect files.
- Use the flat digital cover rather than a physical-book mockup, because the product is an ebook.
- Keep the rest of the resource site's visual language and navigation intact.
- The user authorized the in-chat design: remove the free-resources label in the header and eyebrow, and refresh the ebook card with petroleum green and gold.

## Work units

- [x] **T1 — Remove outdated label.** Remove the header label and its dynamic assignment; replace the home eyebrow without changing resource navigation. Acceptance: no visible "Recursos gratuitos" label on any hash route, and all routes still render. Route: delegated direct, because test and implementation are non-trivial files and preparation spans sibling projects.
- [x] **T2 — Refresh ebook promotion.** Replace the old cover/preview composition with the current flat cover, align card copy and colors with the new landing, and retain the confirmed CTA href. Acceptance: the local cover loads, CTA remains `https://modoverbo.vercel.app/`, and desktop/mobile layout remains usable. Route: delegated direct, because the HTML/CSS, asset, and tests form one cohesive behavior change.

## Verification

- TDD: enabled by the session's strict TDD instruction; observe RED → GREEN → REFACTOR for behavior changes.
- Runner: `python3 -m unittest discover -s tests -v` (new Python standard-library test suite; this repository has no existing runner or dependencies).
- Visual check: inspect the local page at desktop and mobile widths after the change.
- Review mode: off by the user's existing global setting; do not initiate native review.
- Delivery strategy: `ask-on-risk`; forecast under 400 authored changed lines. Track authored additions plus deletions after each commit.

## Progress and evidence

- Branch: `feat/refresh-ebook-cta`, from `093d40af0fe2b9f96b090507f0ed7d8e59d62b7d`.
- T1: removed the header label and its runtime setter; changed the home eyebrow to "Modo Verbo · Practica a tu ritmo". RED observed before implementation. `python3 -m unittest discover -s tests -v`: 3 passed; `git diff --cached --check`: passed. Local browser displayed the new header; an independent local Chrome check confirmed all three hash routes and titles. Native assessment: medium; RDD off, so no review was started. Commit: `1e7b80c8f81b` (`fix(ui): remove free resources label`). Rollback: revert the `index.html` and `tests/test_home_navigation.py` changes in this commit.
- T2: replaced the old brown/yellow two-page card with the new petroleum/gold styling, landing-aligned copy, and flat digital cover. The `?v=e9e38fe4` image URL avoids the stale cover observed in an existing browser cache; the version matches the cover's SHA-256 prefix. RED observed for both the new card and the cache key before implementation. `python3 -m unittest discover -s tests -v`: 6 passed; `git diff --cached --check`: passed. Local desktop screenshot showed the new cover; independent 390px mobile check confirmed image decoding and no horizontal overflow. Native assessment: medium; RDD off, so no review was started. Commit: `7dde90cb3f47` (`feat(ui): refresh ebook promotion`). Rollback: revert this commit, preserving T1.
- Running authored changes: 191 lines (181 additions, 10 deletions) across behavior work-unit commits, plus 36 task-document lines; total delivery diff: 227 lines. Binary cover excluded from this line count.
- Next: user decides whether to push the feature branch or create a pull request; neither has been done.

Repository-relative locator: `odd/tasks/ebook-cta-refresh.md`.
