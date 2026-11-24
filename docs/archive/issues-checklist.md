# Issue Creation Checklist — Avatar: Elements Roadmap

This is a local issue-drafting checklist, not a record of GitHub issues. No issues,
milestones, labels, or project-board fields have been created. Refresh implementation
status and repository ownership before creating any item.

## 1. Before Creating Issues

- [ ] Confirm the current `docs/TASKS.md` status and active branch/work ownership.
- [ ] Review the [project plan](project-plan.md) and decide which release scope is approved.
- [ ] Resolve or explicitly track the open decisions listed in the plan.
- [ ] Confirm repository and GitHub project, milestone/version, labels, and parent-child
  issue support before any remote issue creation.
- [ ] Do not create duplicates of existing `TASKS.md` items; link to existing issues if found.
- [ ] Replace the local keys below with actual issue numbers only after creation.
- [ ] Create tests alongside the feature/enabler they validate, not as an unowned end phase.

## 2. Proposed Issue Order

Priority: P0 blocks dependable work, P1 core, P2 follow-on, P3 optional.  
Estimate: provisional T-shirt size; refine after the issue meets Definition of Ready.

### Epic E0 — Stabilize the vertical-slice baseline

- [ ] **E0** Epic issue — P0, L
  - [ ] **F0.1** Validate active definitions and integration contracts — P0, M
    - [ ] **S0.1.1** Validate skill configuration at load time — P0, M
    - [x] **S0.1.2** Reconcile element-slot assignments — P1, S (conservative placeholder cleanup; final mapping remains subject to review)
    - [ ] **E0.1.3** Resolve cast lifecycle and sustain semantics — P0, M
    - [ ] **E0.1.4** Reconcile PAL dependency metadata — P0, S
    - [ ] **T0.1** Schema and startup validation tests — P0, M
  - [ ] **F0.2** Prove combat synchronization and existing skill behavior — P0, L
    - [ ] **S0.2.1** Verify two-player dedicated-server synchronization — P0, M
    - [ ] **S0.2.2** Verify currently built elemental skills — P0, M
    - [ ] **S0.2.3** Recheck charge/orb lifecycle and Fire Blast — P0, M
    - [ ] **E0.2.4** Reproducible multiplayer test fixture — P0, M
    - [ ] **T0.2** Combat regression suite — P0, M

### Epic E1 — Deliver a coherent four-element combat set

- [ ] **E1** Epic issue — P1, XL (split before scheduling)
  - [ ] **F1.1** Complete the initial elemental ability wave — P1, L
    - [ ] **S1.1.1** Implement and verify Water Jet — P1, M
    - [ ] **S1.1.2** Implement and verify Earth Pillar — P1, M
    - [ ] **S1.1.3** Implement Boulder Launch — P1, M
    - [ ] **S1.1.4** Resolve approved first-wave gaps found by baseline verification — P1, M
    - [ ] **E1.1.5** Shared combat/VFX/audio timeline integration — P1, M
    - [ ] **T1.1** First-wave skill acceptance tests — P1, M
  - [ ] **F1.2** Complete first-release combat and equipment scope — P1, L
    - [ ] **S1.2.1** Finalize hand-to-hand and Air Staff movesets — P1, L
    - [ ] **S1.2.2** Audit armor and weapon bonuses — P1, M
    - [ ] **E1.2.3** Resource and animation integration review — P1, M
    - [ ] **T1.2** Equipment exploit and presentation tests — P1, M

### Epic E2 — Safe material and world interaction

- [ ] **E2** Epic issue — P0/P1, XL (split by W1-W3 gates)
  - [ ] **F2.1** Define ability and world-effect contracts (W1) — P0, M
    - [ ] **E2.1.1** Specify activation/duration/sustain/interruption/source/effects/unlock — P0, M
    - [ ] **E2.1.2** Align config schema, loader, and migration strategy — P0, M
    - [ ] **S2.1.3** Author abilities against the approved contract — P1, M
    - [ ] **T2.1** Contract conformance tests — P0, M
  - [ ] **F2.2** Implement material ledger and transactions (W2) — P0, L
    - [ ] **E2.2.1** Design ledger, persistence, and migration — P0, M
    - [ ] **E2.2.2** Implement atomic transactions and permission checks — P0, L
    - [ ] **S2.2.3** Handle interrupted material abilities — P1, M
    - [ ] **T2.2** Verify conservation and recovery — P0, L
  - [ ] **F2.3** Deliver Earth Wall lifecycle (W3) — P1, L
    - [ ] **S2.3.1** Raise and hold from real material — P1, M
    - [ ] **S2.3.2** Launch and impact the whole wall — P1, L
    - [ ] **S2.3.3** Reclaim, settle, or restore material — P1, M
    - [ ] **E2.3.4** Replicate wall lifecycle to observers — P1, M
    - [ ] **T2.3** Earth Wall multiplayer and conservation tests — P0, L

### Epic E3 — Elemental utilities and progression foundations

- [ ] **E3** Epic issue — P1/P2, XL (split by feature)
  - [ ] **F3.1** Add one server-authoritative utility per element (W4) — P1, L
    - [ ] **S3.1.1** Define utility effects and PvP policy — P0, M
    - [ ] **S3.1.2** Implement approved utility interactions — P1, L
    - [ ] **E3.1.3** Define material tags, volume units, and refill rules (W9) — P0, M
    - [ ] **T3.1** Utility abuse and interaction tests — P1, M
  - [ ] **F3.2** Add profiles, professions, and training (W5) — P2, L
    - [ ] **E3.2.1** Define data, persistence, and migration — P1, M
    - [ ] **S3.2.2** Unlock selective professions and training — P2, L
    - [ ] **S3.2.3** Define ore extraction behavior (W11) — P2, M
    - [ ] **T3.2** Persistence and anti-farming tests — P1, M

### Epic E4 — Confirmed construction and terrain shaping

- [ ] **E4** Epic issue — P2, XL (split before scheduling)
  - [ ] **F4.1** Build preview/confirm and bounded construction (W6) — P2, L
    - [ ] **S4.1.1** Preview changes, material cost, volume, and validation reasons — P2, M
    - [ ] **S4.1.2** Confirm and execute bounded batches — P2, L
    - [ ] **S4.1.3** Recover abandoned or interrupted construction — P2, M
    - [ ] **E4.1.4** Enforce permissions and limits at execution — P1, M
    - [ ] **T4.1** Construction safety and load tests — P1, L

### Epic E5 — Scroll-themed UI and contextual HUD

- [ ] **E5** Epic issue — P1/P2, L
  - [ ] **F5.1** Create functional scroll menu and settings baseline — P1, M
    - [ ] **S5.1.1** Audit HUD, data sources, and input conflicts (UI-01) — P0, S
    - [ ] **S5.1.2** Produce reviewable HUD/menu wireframes (UI-02) — P1, M
    - [ ] **E5.1.3** Implement scalable reusable UI components (UI-03) — P1, L
    - [ ] **E5.1.4** Version preferences and implement apply/cancel/reset (UI-04) — P1, M
    - [ ] **T5.1** UI interaction tests — P1, M
  - [ ] **F5.2** Deliver readable combat HUD and themes — P1, M
    - [ ] **S5.2.1** Display existing live state only (UI-06) — P1, M
    - [ ] **S5.2.2** Implement shared element/tribe themes (UI-05) — P1, M
    - [ ] **E5.2.3** Add accessible visual controls (UI-08) — P1, M
    - [ ] **T5.2** UI compatibility and scale tests (UI-09) — P1, M
  - [ ] **F5.3** Add contextual profile and resource screens — P2, M
    - [ ] **S5.3.1** Show validated profile, mastery, profession, and unlock data (UI-07) — P2, M
    - [ ] **S5.3.2** Show material/construction preview details — P2, M
    - [ ] **T5.3** Dedicated-server permission and stale-data tests — P1, M

### Epic E6 — Beta and release readiness

- [ ] **E6** Epic issue — P0 at release gate, L
  - [ ] **F6.1** Meet multiplayer and performance readiness — P0, L
    - [ ] **E6.1.1** Approve workload and performance budgets — P0, M
    - [ ] **T6.1.2** Run multiplayer/load/compatibility matrix — P0, L
    - [ ] **S6.1.3** Resolve release-blocking defects — P0, variable
  - [ ] **F6.2** Package and document release — P0, M
    - [ ] **E6.2.1** Define client/server packaging and migration policy — P0, M
    - [ ] **S6.2.2** Write install, upgrade, controls, and troubleshooting guidance — P1, M
    - [ ] **T6.2.3** Validate clean install and upgrade — P0, M

## 3. Dependency Links to Record

Create dependency relationships only after both parent/child issues exist.

| Work item | Blocked by |
|---|---|
| E1 combat expansion | E0 multiplayer/schema baseline |
| E2 W1 contract tests | E0 schema and cast lifecycle decisions |
| E2 W2 material ledger | W1 contract and terrain/material decisions |
| E2 W3 Earth Wall | W2 transaction/recovery gate |
| E3 utilities | W1 contract; W2 where material/world mutation is involved |
| E3 progression | Approved persistence, unlock, and anti-farming decisions |
| E4 construction | W2 conservation/recovery; permission and budget decisions |
| E5.1 design and neutral UI components | E0 HUD/input/data audit; may run parallel with W1-W4 |
| E5.2 live HUD | Existing authoritative state sources and E0 validation |
| E5.3 profile/resource UI | E3/E4 data contracts |
| E6 beta/release | Every included feature's tests and integration gates |

## 4. Suggested Labels

Use repository labels if present; do not create labels until repository and naming
conventions are confirmed.

- Type: `epic`, `feature`, `user-story`, `enabler`, `test`
- Priority: `priority-critical`, `priority-high`, `priority-medium`, `priority-low`
- Value: `value-high`, `value-medium`, `value-low`
- Component: `combat`, `schema`, `networking`, `world-interaction`, `progression`,
  `ui`, `assets`, `release`

## 5. Issue Template Minimum Fields

### Epic

- Goal and player value
- Success metrics and high-level acceptance criteria
- Feature children, gates, risks, and estimated size
- Explicit non-goals and release milestone (only if approved)

### Feature

- User-visible outcome
- Story/enabler/test children
- Acceptance criteria and integration/performance expectations
- Blocked-by / blocks dependencies
- Definition of Done and provisional estimate

### Story

- User statement: “As a … I want … so that …”
- Testable acceptance criteria
- Data/security/server-authority impacts
- Test child or named verification requirements
- Dependencies, estimate, and Definition of Done

### Enabler or Test

- Technical or verification outcome, not implementation assumptions alone
- Files/components/data contracts in scope
- Reproducible validation steps and expected evidence
- Dependencies, failure reporting, estimate, and Definition of Done
