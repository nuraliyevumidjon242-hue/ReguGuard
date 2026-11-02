# ReguGuard AI — Local MVP

ReguGuard is a multilingual local implementation of a first end-to-end readiness-screening workflow based on the accompanying technical specification. The interface and reports are available in **English, German, and Uzbek**. Repository inspection, authentication, workspace data, and storage run on your machine.

> **Portfolio presentation:** [Open the interactive EN / DE / UZ project deck](docs/portfolio-presentation.html) (keyboard navigation, responsive layout, and print-to-PDF).

> **Prototype warning:** this is a local MVP, not a production SaaS or a security/compliance audit. It has local accounts, workspace scoping, role checks and an audit hash chain, but has not had an independent security review and does not provide MFA/OIDC, PostgreSQL RLS, managed key service, durable queue, a verified regulatory knowledge base, PDF/A, or a security certification. The server refuses remote binding. Do not upload confidential, production, or real personal data. Findings and legal references are indicative and require qualified human review.

## Run locally

Requirements: Python 3.10 or later. No third-party Python packages, Node.js, external AI API, or build step are required.

```powershell
python app.py
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000). On first run, create the workspace owner with a strong password of at least 12 characters. Add workspace users under **Team & audit**. Stop the server with `Ctrl+C`.

The database is created in `data\reguguard.sqlite3`. To use another local data directory:

```powershell
$env:REGUGUARD_DATA_DIR = "C:\reguguard-local-data"
python app.py
```

The server binds to loopback only and refuses remote binding. Do not override this protection. To remove local records, stop the server, delete only the specific `data\reguguard.sqlite3` file, and restart.

On startup, schema migrations add the account status, scan ownership, audit hashes, and indexes. If an older database has duplicate email addresses (case-insensitive), startup stops with an explicit migration error rather than choosing an account silently. Back up the database and manually resolve the duplicate accounts before restarting.

## What works in this MVP

- Bootstrap a workspace owner; sign in/out with scrypt password hashes, server-side expiring sessions, HttpOnly/SameSite cookies, CSRF tokens, Origin checks, and basic failed-login throttling.
- Add workspace-scoped Admin, Compliance Officer, Developer, and read-only Auditor accounts; deactivate members without deleting audit history and revoke their active sessions. Access checks scope scans, findings, team and audit endpoints to the signed-in workspace.
- Record append-only, per-workspace hash-chained audit events and verify their integrity.
- Upload a ZIP archive and enter intended use, sector, users, and consequential-decision context.
- Enforce upload, ZIP entry, total expanded-size, path traversal, symlink, encrypted archive, and compression-ratio limits. Uploaded source code is inspected as text and **never executed**.
- Detect a small set of possible secrets, email/IBAN patterns, AI framework references, dataset references, and missing basic documentation.
- Mask likely credentials and direct identifiers in saved evidence; raw repository files are held in memory while scanning and are not written to disk.
- Assign an indicative use-case risk screen; conflicting high-impact use-case signals are marked for further review rather than reported as no signal. Review findings, save a human decision/comment, view a localized report, and delete an assessment.
- Print the report or choose “Save as PDF” in the browser print dialog. This is **not PDF/A-2b** and is not a digital signature. The HTTP response provides a SHA-256 integrity header.
- Keep a local SQLite record of workspace, account, scan metadata and redacted finding evidence. Raw repository archive/content is not stored. The UI shows prototype and legal limitations.

This MVP uses deterministic rules, not an LLM. Pattern matching can miss sensitive content and produce false positives. Redaction is not anonymisation. The included legal-reference labels are illustrative, unverified mappings and must not be used as legal advice. SQLite workspace scoping is not PostgreSQL Row-Level Security, password authentication is not MFA or OIDC, and the audit chain is not tamper-proof against an attacker with database-file access.

## API

- `GET /api/health`
- `GET /api/auth/state`
- `POST /api/auth/setup` — one-time first workspace owner bootstrap; JSON: `{"tenant_name":"...","email":"...","password":"..."}`
- `POST /api/auth/login` — JSON: `{"email":"...","password":"..."}`
- `POST /api/auth/logout`
- `GET /api/scans` — authenticated, workspace-scoped
- `POST /api/scans` — `multipart/form-data`: `project_name`, `purpose`, `sector`, optional `users`, optional `consequential_decisions`, and a `.zip` `file`
- `GET /api/scans/{scan_id}`
- `PATCH /api/findings/{finding_id}` — Compliance Officer/Admin/Owner; JSON: `{"status":"open|approved|rejected","comment":"..."}`
- `GET /api/scans/{scan_id}/report?lang=en|de|uz` — localized printable HTML report; SHA-256 integrity digest in `X-Report-SHA256`
- `GET /api/scans/{scan_id}/report?lang=en|de|uz&metadata=1` — report digest and format metadata
- `DELETE /api/scans/{scan_id}` — Compliance Officer/Admin/Owner; removes the scan and findings
- `GET /api/team`, `POST /api/team` — Admin/Owner workspace user management
- `DELETE /api/team/{user_id}` — Owner deactivates a non-owner account and revokes its sessions
- `GET /api/audit`, `GET /api/audit/verify` — workspace audit history and hash-chain verification

Mutating endpoints require the session CSRF token in `X-CSRF-Token` and a same-origin `Origin` header. The API is intentionally local-only; it is not suitable for network deployment.

## Verify

Run the standard-library unit and HTTP workflow tests:

```powershell
python -m unittest discover -s tests -v
```

The tests cover indicative classification, redaction, ZIP path/size/symlink/compression protections, HTML escaping, first-owner setup and login, role permissions, member deactivation/session revocation, tenant isolation, CSRF/Origin enforcement, authenticated upload/review/report/delete, audit-chain verification and tamper detection, report digest, and response security headers.

## Production work still required

Before any real customer use, migrate to the specified Java/Spring Core, Python AI worker, React/TypeScript frontend and PostgreSQL architecture; implement and independently review PostgreSQL RLS and tenant isolation, MFA/OIDC, secure password reset/invitation, production session/key management, encrypted object storage, isolated parsing workers, durable queueing, retention/backups/deletion guarantees, verified and versioned official legal sources, validated localized report content, PDF/A and accessibility checks, benchmark/evaluation datasets, monitoring/incident response, and a threat-modelled deployment. Obtain privacy/legal review and penetration testing. Passing this project's local tests is not evidence that these requirements are complete.
