# RMS Redevelopment Roadmap

Authoritative implementation plan for redeveloping RMS under `socx-platform`'s governance. Approved by the platform owner (2026-08-07) during the SOCX Application Modernisation programme's RMS discovery. This document persists it for real — it previously existed only in conversation history, a gap closed here.

Tracked as `Product: RMS` items in GitHub Project #2 ("SOCX Application Modernisation"). Governed by `socx-platform`'s `ENG-070` (development workflow) and cites the platform's Standards/ADRs/reference implementations throughout rather than restating them.

## Phases

| Phase | Name | Status |
| ----- | ---- | ------ |
| 0 | Foundation | **Done** — `Socx-Org/rms#1` |
| 1 | Infrastructure Alignment | In progress |
| 2A | Structural Refactoring | Not started |
| 2B | Data Layer Modernisation | Not started |
| — | Platform Alignment | Not started (renamed from "Phase 3") |

No phase is blocked by Platform Evolution work unless a dependency is genuinely critical — interim implementations are used and swapped later where a platform capability doesn't exist yet.

### Phase 0 — Foundation (done)

Bring the real RMS codebase into `Socx-Org/rms` as tracked, shared git history, with real, passing test suites. Closed 2026-08-07: `#1`–`#8`, commit `8af6343` (import), `741/741` real tests passing. See `Socx-Org/rms#1` for full success criteria and evidence.

### Phase 1 — Infrastructure Alignment (in progress)

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

### Phase 2A — Structural Refactoring (not started)

Application-level restructuring to align with `ENG-050`/`ENG-060` (repository structure, naming conventions) and any Platform Patterns identified along the way. Scope to be detailed when Phase 1 is substantially through.

### Phase 2B — Data Layer Modernisation (not started)

Resolve the two-ORM situation (Prisma + SQLAlchemy against one database) and align schema-migration practice with the platform's data standards. Scope to be detailed when Phase 2A is substantially through.

### Platform Alignment (not started, renamed from "Phase 3")

Final reconciliation against whatever Platform Patterns / Shared Platform Assets emerged as real, validated capabilities during Phases 1–2B (e.g. Configuration Management, if it graduates from Platform Pattern to Shared Platform Asset per `ADR`/`ENG-070` governance).

## Related Documents

- `socx-platform` ADRs: `ADR-180` (greenfield platform rebuild — defines `prod-lab-01`)
- `socx-platform` reference implementations: `reference/security`, `reference/systemd`, `reference/deployment`, `reference/monitoring`, `reference/nginx`
- `socx-platform` Standards: `ENG-070` (development workflow), `OPS-010`/`OPS-030`/`OPS-040`/`OPS-050`
- `Socx-Org/rms#1` — Phase 0 (Foundation) Epic, closed
