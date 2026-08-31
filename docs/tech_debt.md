# Technical Debt
1. ~~Investigate (A MUST DO): The one failure (outbox.test.js — "worker consumes outbox row")~~ **FIXED** — `process_outbox_once.py` now drains all pending rows in a loop (batch_size=100) instead of a single fixed pass of 50, and `process_outbox()` returns the row count to support this. 165/165 passing.
2. ~~ci.yml / deploy.yml broken~~ **FIXED** — see below.
3. Add Typescript for email
3. Add TypeScript for api
4. add OpenAPI docs updates or implement pagination meta in responses.
5. Upgrade `react-router-dom` 6.x -> 7.x (`rms#16`'s npm audit triage): the only 2 vulnerabilities `npm audit` can't resolve without `--force` are both in `react-router`/`react-router-dom`, and the fix is a real semver-major migration (React Router v6 -> v7's API changes), not a routine dependency bump -- deliberately deferred out of that triage pass rather than done without real testing. 