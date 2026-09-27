# Feature the latest resource on the home page

## Objective

Place a prominent latest-resource banner immediately after the home introduction, present the existing resources in a one-per-row list, and polish the ebook CTA as requested during implementation. The current latest resource is “Cómo mejorar tu forma de hablar” at `#guia`.

## Problem and why

The current home page moves directly from its introduction to a two-column catalog. The user wants visitors to encounter the newest resource first, while keeping the full numbered catalog below.

## Scope and constraints

- Authorized: local homepage presentation changes in this repository, as approved in chat.
- Not authorized: remote Git operations, deployment, or changes to sibling projects.
- Featured banner copy must describe the currently available diagnostic, not imply the full speaking guide is complete.
- Preserve resources 01–04, all hash routes, the coming-soon status of 04, and the ebook promotion.
- Keep the existing visual identity and support mobile/desktop, keyboard focus, and readable hierarchy.
- The site is static: the featured resource is intentionally maintained alongside the catalog when a new resource is added; no CMS or automatic “latest” detector is introduced.
- The approved ebook CTA polish centers copy on mobile while preserving the readable desktop layout, and pairs the existing flat cover with one restrained local interior preview. Do not add unverified author/physical-book imagery.
- The approved featured-card animation is a slow, subtle orange glow along the full card border: no harsh blinking, no layout shift, and no animation on the CTA or text. Disable motion when `prefers-reduced-motion: reduce` is active while keeping the card statically highlighted.
- Effective TDD: enabled by project instructions (`gentle-ai:strict-tdd-mode`); runner: `python3 -m unittest discover -s tests -v`.
- Delivery strategy: `ask-on-risk` default. Revised forecast: about 350–450 authored changed lines across all work units; the ~400-line PR planning heuristic is advisory, not a code-size target. No PR or push is requested.

## Tasks

- [x] **T1 — Featured latest-resource banner.** Add an accessible featured block between the home hero and resource catalog, linked to `#guia`, with title, concise diagnostic-specific copy, and clear CTA. Route: delegated writer; triggers: source preparation and non-trivial HTML/CSS plus tests. Acceptance: banner is first below the intro; link navigates to the current guide; wording does not claim the full guide exists. Checks: focused test RED/GREEN, full unittest suite, `git diff --check`, desktop/mobile browser check. Commit: `a84f50c0aa40e9c43a93e522ef8ea1a4f94e4696`.
- [x] **T2 — One-resource-per-row catalog.** Convert the four numbered cards below the banner into full-width rows without losing their order, navigation, or unavailable status; check responsive layout and preserve the ebook promotion. Route: delegated writer; triggers: source preparation plus tests and visual QA. Acceptance: cards 01–04 each occupy a distinct row at desktop and mobile widths; the two existing routes and guide link still work; 04 is not clickable. Checks: focused test RED/GREEN, full unittest suite, `git diff --check`, desktop/mobile browser check. Commit: `e2ad2ec62f51f809e34b8afd8e5954a371c642bf`.
- [x] **T3 — Ebook CTA polish.** Center the ebook CTA copy on mobile, retain left-aligned copy on desktop, and layer the existing local interior preview behind the flat cover without clutter or layout overflow. Route: delegated writer; triggers: multiple non-trivial files and visual verification. Acceptance: existing ebook destination remains unchanged; copy and image composition are coherent at mobile and desktop widths; no external imagery or claims of a physical book are introduced. Checks: focused test RED/GREEN, full unittest suite, `git diff --check`; rendered desktop/mobile visual review unavailable because local-file browser access was denied. Commit: `3d2d316344cd2160f7f5bb7c507c4a938cbd3bdd`.
- [ ] **T4 — Featured-card motion.** Add a slow, subtle orange glow along the full featured-card border; avoid harsh blinking, layout shifts, and motion on the CTA or text. Disable the animation for `prefers-reduced-motion: reduce`, leaving a static orange border highlight. Route: delegated writer; triggers: source preparation and focused CSS regression coverage. Acceptance: only the featured card's border glow animates; timing is slow and continuous; reduced-motion users see a static highlight; layout and content remain stationary. Checks: focused test RED/GREEN, full unittest suite, `git diff --check`, and browser animation inspection at 390px and 1280px only if normal local-file browser access is allowed. Commit: pending.

## Progress and evidence

- 2026-09-27: User approved bounded design. Base `main` at `c84a97f`; created `feat/featured-resource-home`. Baseline: 11/11 unittest tests passed.
- T1: RED observed before implementation; 3/3 focused tests and 14/14 full tests passed. Independent headless checks at 1280px and 390px confirmed banner adjacency, CTA click to `#guia`, no horizontal overflow, and preserved catalog/ebook. Staged diff check passed. Native risk tier: medium; receipt-driven development off globally, so no native review. Work-unit commit `a84f50c` (143 changed lines). Rollback: revert this commit to remove banner and its focused tests without affecting existing resources.
- T2: Browser probe RED measured two desktop rows before implementation, then GREEN measured four distinct full-width rows at 1280px and 390px with no horizontal overflow. Full unittest suite passed 15/15; staged diff check passed. Independent static review found no confirmed defect but could not repeat browser inspection because its browser denied the local file; it noted that the automated tests do not assert row geometry. Native risk tier: medium; receipt-driven development off globally, so no native review. Work-unit commit `e2ad2ec` (108 changed lines). Rollback: revert this commit to restore the earlier grid while preserving the featured banner.
- T3: Focused TDD exposed the need for mobile centering and a preview. Independent verification then found the initial preview nearly hidden, so the writer added a RED geometry regression test before correcting its width and offset. Final suite passed 17/17; staged diff check passed. Static geometry shows approximately 31% of the decorative interior page exposed at both 230px and 300px figure sizes, without likely horizontal overflow; destination and descriptive cover alt remain intact. Rendered visual/keyboard review remains unavailable due to denied local-file browser access and was not bypassed. Native risk tier: medium; receipt-driven development off globally. Work-unit commit `3d2d316` (40 changed lines). Rollback: revert this commit to restore the previous single-cover layout.

## Next step

Obtain a scoped design decision before implementing T4. Rendered desktop/mobile QA for T3 remains pending until an allowed browser path is available. No remote publication without separate authorization.
