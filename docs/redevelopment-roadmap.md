# RMS Redevelopment Roadmap

Authoritative implementation plan for redeveloping RMS under `socx-platform`'s governance. Approved by the platform owner (2026-08-07) during the SOCX Application Modernisation programme's RMS discovery. This document persists it for real — it previously existed only in conversation history, a gap closed here.

Tracked as `Product: RMS` items in GitHub Project #2 ("SOCX Application Modernisation"). Governed by `socx-platform`'s `ENG-070` (development workflow) and cites the platform's Standards/ADRs/reference implementations throughout rather than restating them.

## Phases

| Phase | Name | Status |
| ----- | ---- | ------ |
| 0 | Foundation | **Done** — `Socx-Org/rms#1` |
| 1 | Infrastructure Alignment | **Done** — `Socx-Org/rms#9` |
| 2A | Structural Refactoring | **Done** — `Socx-Org/rms#17` |
| 2B | Data Layer Modernisation | **Closed** — resolved at the platform level, no RMS code change required (`socx-platform#94`/`ADR-200`) |
| — | Platform Alignment | **Done** — `socx-platform#97` (renamed from "Phase 3") |

No phase is blocked by Platform Evolution work unless a dependency is genuinely critical — interim implementations are used and swapped later where a platform capability doesn't exist yet.

### Phase 0 — Foundation (done)

Bring the real RMS codebase into `Socx-Org/rms` as tracked, shared git history, with real, passing test suites. Closed 2026-08-07: `#1`–`#8`, commit `8af6343` (import), `741/741` real tests passing. See `Socx-Org/rms#1` for full success criteria and evidence.

### Phase 1 — Infrastructure Alignment (done)

**Finding that reshapes this phase's scope (2026-08-08, re-verified directly against real repo/infra state before starting):** RMS has never actually been deployed to `prod-lab-01`, the platform's real rebuilt droplet (`ADR-180`) — its hostname currently returns a clean `502`; nginx is configured and TLS is live (`reference/nginx/sites/rms.conf` already deployed), nothing is listening behind it. This is RMS's *first* real deployment, not a migration of an already-running production app. The platform's reference implementations for exactly this (`reference/security`, `reference/systemd`, `reference/deployment`, `reference/monitoring`, `reference/nginx`) are already Approved, and in nginx's/monitoring's case already live against RMS's own hostname — so "edge/TLS migration" is effectively already done at the infra level. The real work is getting RMS's app to stand up behind what already exists, replacing the bespoke mechanisms below with the platform's reference implementations rather than continuing to build the bespoke path out further.

**What's bespoke and misaligned today (re-verified 2026-08-08):**
- `.github/workflows/deploy.yml` does on-host `npm ci` at deploy time with no versioned release and no rollback; it was written against a different, earlier environment and needs a full rewrite, not a patch, to deploy correctly to `prod-lab-01`.
- No GitHub Environment or secrets exist for RMS at all (`gh secret list` / `gh api .../environments` both empty) — the deploy pipeline has never actually run to completion.
- Production application secrets (`DATABASE_URL`, `JWT_SECRET`, SMTP credentials) rely on hand-placed `.env` files with no managed provisioning mechanism.
- No `systemd` units exist matching `reference/systemd`'s versioned-release pattern.
- `deploy.conf` (repo root) and the `deploy.yml` step referencing `do-nginx-infra`'s `nginx-config` branch both target a different, legacy on-host deploy mechanism (`/opt/infra/scripts/deploy.sh`) that `reference/deployment`'s actual scripts don't use — dead configuration from the prior infra pattern, to be retired, not preserved.
- No application health endpoint exists matching `reference/monitoring/http/health-router.ts` — `reference/deployment`'s health gate and the already-live uptime checks currently have nothing app-specific to check against.

**Sub-issues:**

1. **Secrets** — provision RMS's production secrets via `reference/security`'s mechanism (`set-credential.sh`, root-only credentials directory, `LoadCredential=`), replacing hand-placed `.env` files on the host.
2. **Systemd units** — add `rms-api`/`rms-worker` units per `reference/systemd`'s versioned-release layout (`/opt/rms/releases/<version>`, `current` symlink).
3. **Deploy mechanism** — rewrite `deploy.yml` to build a release tarball and invoke `reference/deployment/scripts/deploy-release.sh`/`rollback.sh` against `prod-lab-01`, removing `deploy.conf` and the dead `do-nginx-infra` reference. Provision the missing GitHub Environment/secrets (`DROPLET_HOST`, `DROPLET_USER`, `DROPLET_SSH_KEY`) for real, pointed at `prod-lab-01`'s confirmed address.
4. **Health endpoint & monitoring alignment** — add a `/healthz` route per `reference/monitoring/http/health-router.ts` so `reference/deployment`'s health gate and the already-live DigitalOcean uptime checks have something real to check.

**Success criteria:** RMS's API and worker run as real, versioned `systemd` services on `prod-lab-01`; a deploy is a real `deploy-release.sh` invocation with an automatic-rollback health gate, not an in-place `npm ci`; production secrets are provisioned via `reference/security`, not hand-placed; the existing DigitalOcean uptime check for `rms` reports real `UP` status.

**Closed 2026-08-08, `Socx-Org/rms#9`, all five sub-issues (`#10`–`#14`).** All success criteria met with real evidence — see the Epic's own closing evidence for the full list. RMS is live in production at `https://rms.socx.org.uk` (API, worker, and web frontend), for the first time in its history.

### Phase 2A — Structural Refactoring (done)

Real discovery against `ENG-050`/`ENG-060` and the relevant reference implementations (`reference/application`, `reference/systemd`, `reference/nginx`), not assumed. Most apparent gaps resolved on inspection — RMS's monorepo layout, unprefixed env vars, and test locations all already matched `reference/application`'s own convention.

Two genuine RMS-owned findings, both fixed: no `LICENSE` file (`ENG-050.1`) — added, proprietary/internal, copyright holder Socx Organisation (SOCX software is confirmed not open source; `socx-platform`'s own `LICENSE` was also corrected to match); four dead legacy artifacts (`infra/pm2/`, `infra/supervisor/`, `infra/scripts/bootstrap-server.sh`, stale `infra/nginx/rms.conf`) removed, plus a real `README.md` accuracy pass (actual Node 24/Python 3.14, actual `systemd`+`deploy-release.sh` mechanism, actual hand-rolled-poll-loop worker, not APScheduler).

Two genuine platform-level findings deliberately routed to Platform Evolution instead of RMS's own backlog — RMS stayed unchanged pending those: `ENG-060.4`'s infra-naming rule doesn't match `reference/systemd`/`reference/nginx`'s own actual naming (`socx-platform#89`, still open); the `LoadCredential=` env-var shim (`credentials.js`/`credentials.py`, from Phase 1's `#10`) as a candidate Platform Pattern (`socx-platform#90`, still open).

**Closed 2026-08-08, `Socx-Org/rms#17`, both sub-issues (`#18`, `#19`).**

### Phase 2B — Data Layer Modernisation (closed, no RMS code change)

Originally framed as "resolve the two-ORM situation (Prisma + SQLAlchemy against one database)." Real investigation found this framing didn't hold up: RMS's worker doesn't actually use SQLAlchemy as an ORM (no model classes, just raw SQL via `text()` queries), and — more importantly — the platform's own `ADR-090` had explicitly, deliberately deferred the Prisma-vs-raw-SQL decision to "a dedicated future ADR" that didn't exist yet. This was never RMS's decision to make unilaterally, the same governance principle already applied to Phase 2A's `ENG-060.4` finding.

Routed to Platform Evolution as a Spike (`socx-platform#94`), which produced `ADR-200`: the platform default going forward is raw SQL + a repository pattern (matching `reference/application`), not Prisma platform-wide — **but RMS's existing, live Prisma usage is explicitly, deliberately exempted, not required to migrate.** `ADR-090` amended to record the resolution.

**Net effect: Phase 2B closes with zero RMS code changes.** The "problem" was resolved by naming and formally accepting the divergence, not by migrating away from it.

Separately, real discovery during this phase found RMS's production database has **zero backup coverage** (`OPS-060.1` violation, confirmed directly on `prod-lab-01`) — tracked as `Socx-Org/rms#24`, deliberately deferred by the platform owner until RMS has real user data worth protecting (currently 1 account). Not part of Phase 2B's original scope, surfaced by the same investigation.

**Closed 2026-08-08.**

### Platform Alignment (done, renamed from "Phase 3")

Final reconciliation against whatever Platform Patterns / Shared Platform Assets emerged as real, validated capabilities during Phases 1–2B. Real discovery (2026-08-08) checked three candidates from RMS's actual work, not assumed:

- **Configuration Management** (`system_settings`) — real, validated within RMS across two runtimes (API + worker), but the programme's own "validated across ≥2 apps" graduation criterion isn't met (RMS is still the only real, live application). Documented as an early Platform Pattern, not promoted to a Shared Platform Asset: `socx-platform`'s `APP-020`.
- **`reference/deployment`'s Python-worker rollback limitation** — real, already self-documented in RMS's own `deploy.yml` comments, never fed back to the platform. Recorded in `reference/deployment/README.md`'s own Design Decisions, not fixed (no second real Python-worker deployment exists yet to validate a general solution against).
- **`reference/nginx`'s static/API split** — checked, found to be a non-issue: its own "Expected Adaptations" section already anticipated exactly this per-app customisation; RMS's real split (`#14`) is that working as designed, not a missing pattern.

**Closed 2026-08-08, `socx-platform#97`, merged as PR #98.**

**This closes the RMS Redevelopment Roadmap.** All phases (0, 1, 2A, 2B, Platform Alignment) are done. Remaining open items are tracked separately, not blocking: `Socx-Org/rms#24` (backups, deliberately deferred pending real user data).

## Related Documents

- `socx-platform` ADRs: `ADR-180` (greenfield platform rebuild — defines `prod-lab-01`)
- `socx-platform` reference implementations: `reference/security`, `reference/systemd`, `reference/deployment`, `reference/monitoring`, `reference/nginx`
- `socx-platform` Standards: `ENG-070` (development workflow), `OPS-010`/`OPS-030`/`OPS-040`/`OPS-050`
- `Socx-Org/rms#1` — Phase 0 (Foundation) Epic, closed
