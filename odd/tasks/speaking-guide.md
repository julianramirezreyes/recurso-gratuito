# Practical speaking guide

## Objective

Turn home resource 03 into a complete, practice-first Spanish guide titled “Cómo mejorar tu forma de hablar”, and move the existing “Próximamente” card to resource 04. Preserve resources 01 and 02 and the ebook promotion.

## Problem and why

Resource 03 is currently only a placeholder. The user supplied a detailed brief for a high-value guide that helps readers diagnose and practice clarity, fluency, diction, voice, organization, improvisation, vocabulary, confidence, and public speaking without generic advice.

## Scope and constraints

- Authorized: local implementation of the approved guide design and home-card order in this repository.
- Not authorized by this request: remote Git operations, deployment, or modifying sibling projects.
- Keep the existing hash-based resource navigation and visual language; make the guide mobile-first and accessible.
- Ground material recommendations in reliable primary sources; distinguish evidence limitations without turning the guide into an academic article.
- Make each important exercise specify what to do, how long, what to observe, and how to judge progress.
- Preserve all existing resources and ebook links.
- Effective TDD: enabled by project instructions (`gentle-ai:strict-tdd-mode`); runner: `python3 -m unittest discover -s tests -v`.
- Delivery strategy: `ask-on-risk` (default); no PR requested. Forecast: approximately 700–1,100 authored lines, excluding generated assets. This is an estimate, not a size target; do not compress prose or omit tests to fit a budget.

## Tasks

- [ ] **T1 — Navigation and diagnostic.** Replace home slot 03 with an active guide card, add slot 04 “Próximamente”, add a usable guide entry/diagnostic and route, and cover navigation with tests. Route: delegated writer; triggers: source preparation, multiple non-trivial files. Acceptance: cards 01–04 appear in order; 03 opens the guide; 04 remains unavailable; existing routes and ebook promotion work. Checks: focused tests, full unittest suite, `git diff --check`, local browser navigation. Commit: pending.
- [ ] **T2 — Practice content and progression.** Complete the seven core skills, supporting sections from the brief, five-minute routine, seven-day challenge, final self-test, practical examples, and modest interactive progress/reveal controls; attach source notes and tests where behavior warrants them. Route: delegated writer; triggers: substantial content and multiple non-trivial files. Acceptance: every requested area is covered with actionable practice and honest caveats; progress survives refresh if local storage is available; no unrelated content is removed. Checks: focused behavior tests, full unittest suite, `git diff --check`, desktop/mobile visual and interaction review. Commit: pending.

## Progress and evidence

- 2026-09-25: User approved bounded design. Base `main` at `d918ec8`; feature branch `feat/speaking-guide` created. Baseline: 8/8 unittest tests passed.
- Source-backed research memo gathered from Stanford, ASHA, and primary studies; practical adaptations and evidence limits identified for T2.
- T1 implementation and independent local verification complete but not committed: 11/11 unittest tests passed, staged diff check passed, desktop/mobile and direct `#guia` smoke checks passed. Balanced desktop grid changed to two columns; parent reran 11/11 tests and inspected a 1280px screenshot. New static parser tests do not cover click/keyboard behavior; no blocking finding. Commit pending the delivery-strategy decision.

## Next step

Resolve the delivery-strategy choice required by the >400-line feature forecast, then close T1 with a work-unit commit. Delegate T2 with strict RED → GREEN → REFACTOR. Do not publish remotely without a separate authorization.
