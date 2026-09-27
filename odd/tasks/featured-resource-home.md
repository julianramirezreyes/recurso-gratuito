# Feature the latest resource on the home page

## Objective

Place a prominent latest-resource banner immediately after the home introduction, then present the existing resources in a one-per-row list. The current latest resource is “Cómo mejorar tu forma de hablar” at `#guia`.

## Problem and why

The current home page moves directly from its introduction to a two-column catalog. The user wants visitors to encounter the newest resource first, while keeping the full numbered catalog below.

## Scope and constraints

- Authorized: local homepage presentation changes in this repository, as approved in chat.
- Not authorized: remote Git operations, deployment, or changes to sibling projects.
- Featured banner copy must describe the currently available diagnostic, not imply the full speaking guide is complete.
- Preserve resources 01–04, all hash routes, the coming-soon status of 04, and the ebook promotion.
- Keep the existing visual identity and support mobile/desktop, keyboard focus, and readable hierarchy.
- The site is static: the featured resource is intentionally maintained alongside the catalog when a new resource is added; no CMS or automatic “latest” detector is introduced.
- Effective TDD: enabled by project instructions (`gentle-ai:strict-tdd-mode`); runner: `python3 -m unittest discover -s tests -v`.
- Delivery strategy: `ask-on-risk` default. Forecast: about 120–250 authored changed lines, below the ~400-line PR planning heuristic. No PR or push is requested.

## Tasks

- [x] **T1 — Featured latest-resource banner.** Add an accessible featured block between the home hero and resource catalog, linked to `#guia`, with title, concise diagnostic-specific copy, and clear CTA. Route: delegated writer; triggers: source preparation and non-trivial HTML/CSS plus tests. Acceptance: banner is first below the intro; link navigates to the current guide; wording does not claim the full guide exists. Checks: focused test RED/GREEN, full unittest suite, `git diff --check`, desktop/mobile browser check. Commit: `a84f50c0aa40e9c43a93e522ef8ea1a4f94e4696`.
- [ ] **T2 — One-resource-per-row catalog.** Convert the four numbered cards below the banner into full-width rows without losing their order, navigation, or unavailable status; check responsive layout and preserve the ebook promotion. Route: delegated writer; triggers: source preparation plus tests and visual QA. Acceptance: cards 01–04 each occupy a distinct row at desktop and mobile widths; the two existing routes and guide link still work; 04 is not clickable. Checks: focused test RED/GREEN, full unittest suite, `git diff --check`, desktop/mobile browser check. Commit: pending.

## Progress and evidence

- 2026-09-27: User approved bounded design. Base `main` at `c84a97f`; created `feat/featured-resource-home`. Baseline: 11/11 unittest tests passed.
- T1: RED observed before implementation; 3/3 focused tests and 14/14 full tests passed. Independent headless checks at 1280px and 390px confirmed banner adjacency, CTA click to `#guia`, no horizontal overflow, and preserved catalog/ebook. Staged diff check passed. Native risk tier: medium; receipt-driven development off globally, so no native review. Work-unit commit `a84f50c` (143 changed lines). Rollback: revert this commit to remove banner and its focused tests without affecting existing resources.

## Next step

Delegate T2 through strict RED → GREEN → REFACTOR; verify and commit its work unit. No remote publication without separate authorization.
