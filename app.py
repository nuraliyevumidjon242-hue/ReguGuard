from __future__ import annotations

import hashlib
import html
import json
import os
import re
import secrets
import sqlite3
import threading
import time
import uuid
import zipfile
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from email import policy
from email.parser import BytesParser
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from urllib.parse import parse_qs, unquote, urlparse


ROOT = Path(__file__).resolve().parent
WEB_ROOT = ROOT / "web"
DATA_DIR = Path(os.environ.get("REGUGUARD_DATA_DIR", ROOT / "data")).resolve()
DB_PATH = DATA_DIR / "reguguard.sqlite3"
MAX_UPLOAD_BYTES = 25 * 1024 * 1024
MAX_FILES = 2_000
MAX_EXPANDED_BYTES = 50 * 1024 * 1024
MAX_FILE_BYTES = 2 * 1024 * 1024
MAX_FINDINGS = 200
SESSION_TTL_SECONDS = 8 * 60 * 60
PASSWORD_MIN_LENGTH = 12
ALLOWED_EXTENSIONS = {
    ".py", ".java", ".kt", ".js", ".jsx", ".ts", ".tsx", ".go", ".rs",
    ".php", ".rb", ".cs", ".json", ".yaml", ".yml", ".toml", ".xml",
    ".md", ".txt", ".sql", ".env", ".env.example", ".properties", ".cfg", ".ini",
}
SKIP_PARTS = {".git", "node_modules", "vendor", ".venv", "venv", "dist", "build"}
AUTH_FAILURES: dict[str, list[float]] = {}
AUTH_FAILURES_LOCK = threading.Lock()

RULES = {
    "secret": {
        "severity": "critical",
        "regulation": "GDPR Art. 32 (security review; applicability requires human assessment)",
    },
    "personal_data": {
        "severity": "medium",
        "regulation": "GDPR Art. 5(1)(c), Art. 25 (data minimisation and protection by design; verify context)",
    },
    "sensitive_data": {
        "severity": "high",
        "regulation": "GDPR Art. 9 (special-category data; confirm whether data is personal and applicable)",
    },
    "ai_dependency": {
        "severity": "low",
        "regulation": "EU AI Act Art. 3 and Art. 6 / Annex III (scope and classification depend on intended purpose)",
    },
    "dataset_reference": {
        "severity": "medium",
        "regulation": "GDPR Art. 5 and Art. 9 (dataset contents and processing purpose require review)",
    },
    "missing_docs": {
        "severity": "low",
        "regulation": "EU AI Act Art. 11 / Annex IV (only where the relevant high-risk requirements apply)",
    },
}

SECRET_PATTERNS = [
    re.compile(r"(?i)(?:api[_-]?key|secret|password|token|private[_-]?key)\s*[:=]\s*['\"]?([A-Za-z0-9_./+=-]{8,})"),
    re.compile(r"\b(?:sk-[A-Za-z0-9_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})\b"),
]
EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
IBAN_RE = re.compile(r"\b[A-Z]{2}\d{2}(?:[\s-]?[A-Z0-9]){11,30}\b", re.I)
PHONE_RE = re.compile(r"(?<!\w)(?:\+\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?){2,4}\d{2,4}(?!\w)")
SOURCE_DATA_RE = re.compile(r"(?i)\b(?:health|medical|diagnos|religion|ethnic|biometric|political)[\w -]{0,24}\b")
AI_RE = re.compile(
    r"(?i)\b(?:langchain|transformers|torch|pytorch|tensorflow|scikit.learn|"
    r"openai|anthropic|llamaindex|google.generativeai)\b"
)
DATASET_RE = re.compile(r"(?i)\b(?:dataset|training[_ -]?data|patient[_ -]?data|customer[_ -]?data)\b")


class RequestError(Exception):
    def __init__(self, status: int, message: str):
        super().__init__(message)
        self.status = status


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


@contextmanager
def database():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    connection.execute("PRAGMA busy_timeout = 10000")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def initialise_database() -> None:
    with database() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS tenants (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS app_users (
                id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
                email TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('owner','admin','compliance_officer','developer','auditor')),
                active INTEGER NOT NULL DEFAULT 1 CHECK(active IN (0,1)),
                created_at TEXT NOT NULL,
                UNIQUE(tenant_id, email)
            );
            CREATE TABLE IF NOT EXISTS sessions (
                token_hash TEXT PRIMARY KEY,
                user_id TEXT NOT NULL REFERENCES app_users(id) ON DELETE CASCADE,
                csrf_token TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS scans (
                id TEXT PRIMARY KEY,
                tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
                created_by TEXT NOT NULL REFERENCES app_users(id),
                project_name TEXT NOT NULL,
                purpose TEXT NOT NULL,
                sector TEXT NOT NULL,
                users TEXT NOT NULL,
                consequential_decisions INTEGER NOT NULL,
                risk_category TEXT NOT NULL,
                status TEXT NOT NULL,
                file_count INTEGER NOT NULL,
                created_at TEXT NOT NULL
            );
            CREATE INDEX IF NOT EXISTS idx_scans_tenant_created ON scans(tenant_id, created_at);
            CREATE TABLE IF NOT EXISTS findings (
                id TEXT PRIMARY KEY,
                scan_id TEXT NOT NULL REFERENCES scans(id) ON DELETE CASCADE,
                rule_key TEXT NOT NULL,
                severity TEXT NOT NULL,
                file_path TEXT NOT NULL,
                line_number INTEGER NOT NULL,
                evidence TEXT NOT NULL,
                regulation TEXT NOT NULL,
                review_status TEXT NOT NULL DEFAULT 'open',
                comment TEXT NOT NULL DEFAULT ''
            );
            CREATE INDEX IF NOT EXISTS idx_findings_scan ON findings(scan_id);
            CREATE TABLE IF NOT EXISTS audit_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tenant_id TEXT NOT NULL REFERENCES tenants(id) ON DELETE CASCADE,
                actor_id TEXT NOT NULL REFERENCES app_users(id),
                action TEXT NOT NULL,
                target_id TEXT,
                created_at TEXT NOT NULL,
                previous_hash TEXT,
                event_hash TEXT
            );
            CREATE TRIGGER IF NOT EXISTS audit_events_no_update
            BEFORE UPDATE ON audit_events BEGIN SELECT RAISE(ABORT, 'audit events are append-only'); END;
            CREATE TRIGGER IF NOT EXISTS audit_events_no_delete
            BEFORE DELETE ON audit_events BEGIN SELECT RAISE(ABORT, 'audit events are append-only'); END;
            """
        )
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(scans)")}
        user_columns = {row["name"] for row in connection.execute("PRAGMA table_info(app_users)")}
        if "active" not in user_columns:
            connection.execute("ALTER TABLE app_users ADD COLUMN active INTEGER NOT NULL DEFAULT 1")
        if "tenant_id" not in columns:
            connection.execute("ALTER TABLE scans ADD COLUMN tenant_id TEXT REFERENCES tenants(id)")
        if "created_by" not in columns:
            connection.execute("ALTER TABLE scans ADD COLUMN created_by TEXT REFERENCES app_users(id)")
        audit_columns = {row["name"] for row in connection.execute("PRAGMA table_info(audit_events)")}
        if "previous_hash" not in audit_columns:
            connection.execute("ALTER TABLE audit_events ADD COLUMN previous_hash TEXT")
        if "event_hash" not in audit_columns:
            connection.execute("ALTER TABLE audit_events ADD COLUMN event_hash TEXT")
        duplicate_emails = connection.execute(
            """SELECT COUNT(*) FROM (
                SELECT email FROM app_users GROUP BY email COLLATE NOCASE HAVING COUNT(*) > 1
            )"""
        ).fetchone()[0]
        if duplicate_emails:
            raise RuntimeError(
                "Database migration cannot enforce unique sign-in emails because duplicate accounts exist. "
                "Resolve duplicate email addresses in the existing database, then restart ReguGuard."
            )
        connection.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_app_users_email_global ON app_users(email COLLATE NOCASE)"
        )
        connection.execute("CREATE INDEX IF NOT EXISTS idx_sessions_expiry ON sessions(expires_at)")


def password_hash(password: str, salt: bytes | None = None) -> str:
    salt = salt or secrets.token_bytes(16)
    derived = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=2**14, r=8, p=1, dklen=64)
    return f"scrypt${salt.hex()}${derived.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, salt_hex, digest_hex = encoded.split("$", 2)
        if algorithm != "scrypt":
            return False
        derived = hashlib.scrypt(
            password.encode("utf-8"), salt=bytes.fromhex(salt_hex), n=2**14, r=8, p=1, dklen=64
        )
        return secrets.compare_digest(derived.hex(), digest_hex)
    except (ValueError, TypeError):
        return False


DUMMY_PASSWORD_HASH = password_hash("invalid-login-timing-placeholder")


def audit(connection: sqlite3.Connection, tenant_id: str, actor_id: str, action: str, target_id: str | None = None) -> None:
    created = now_iso()
    previous_row = connection.execute(
        "SELECT event_hash FROM audit_events WHERE tenant_id=? ORDER BY id DESC LIMIT 1", (tenant_id,)
    ).fetchone()
    previous_hash = previous_row["event_hash"] if previous_row else "GENESIS"
    payload = json_bytes({
        "tenant_id": tenant_id, "actor_id": actor_id, "action": action,
        "target_id": target_id, "created_at": created, "previous_hash": previous_hash,
    })
    event_hash = hashlib.sha256(payload).hexdigest()
    connection.execute(
        """INSERT INTO audit_events
        (tenant_id,actor_id,action,target_id,created_at,previous_hash,event_hash) VALUES (?,?,?,?,?,?,?)""",
        (tenant_id, actor_id, action, target_id, created, previous_hash, event_hash),
    )


def register_auth_failure(key: str) -> bool:
    now = time.monotonic()
    with AUTH_FAILURES_LOCK:
        recent = [item for item in AUTH_FAILURES.get(key, []) if now - item < 900]
        recent.append(now)
        AUTH_FAILURES[key] = recent
        if len(AUTH_FAILURES) > 2_000:
            expired_keys = [entry for entry, values in AUTH_FAILURES.items() if not values or now - values[-1] >= 900]
            for entry in expired_keys:
                AUTH_FAILURES.pop(entry, None)
        return len(recent) >= 5


def clear_auth_failures(key: str) -> None:
    with AUTH_FAILURES_LOCK:
        AUTH_FAILURES.pop(key, None)


def redact(text: str) -> str:
    value = text
    for pattern in SECRET_PATTERNS:
        value = pattern.sub("[REDACTED_SECRET]", value)
    value = EMAIL_RE.sub("[REDACTED_EMAIL]", value)
    value = IBAN_RE.sub("[REDACTED_IBAN]", value)
    value = PHONE_RE.sub("[REDACTED_PHONE]", value)
    return value[:500]


def safe_zip_texts(archive_bytes: bytes) -> list[tuple[str, str]]:
    try:
        archive = zipfile.ZipFile(__import__("io").BytesIO(archive_bytes))
    except (zipfile.BadZipFile, OSError):
        raise RequestError(400, "The uploaded file is not a valid ZIP archive.")

    texts: list[tuple[str, str]] = []
    infos = archive.infolist()
    if len(infos) > MAX_FILES:
        raise RequestError(413, f"ZIP contains more than {MAX_FILES} entries.")

    expanded = 0
    for info in infos:
        raw_name = info.filename
        path = PurePosixPath(raw_name)
        mode = (info.external_attr >> 16) & 0xFFFF
        if (
            path.is_absolute()
            or "\\" in raw_name
            or bool(re.match(r"^[A-Za-z]:", raw_name))
            or any(part in {"..", ""} for part in path.parts)
            or (mode & 0o170000) == 0o120000
        ):
            raise RequestError(400, "ZIP contains an unsafe path or symbolic link.")
        if info.flag_bits & 0x1:
            raise RequestError(400, "Encrypted ZIP entries are not supported.")
        if info.is_dir() or any(part.lower() in SKIP_PARTS for part in path.parts):
            continue
        if info.file_size > MAX_FILE_BYTES:
            raise RequestError(413, "A ZIP entry exceeds the 2 MiB per-file limit.")
        expanded += info.file_size
        if expanded > MAX_EXPANDED_BYTES:
            raise RequestError(413, "ZIP exceeds the 50 MiB expanded-size limit.")
        if info.file_size > 1_000_000 and info.compress_size and info.file_size / info.compress_size > 100:
            raise RequestError(413, "ZIP contains an entry with a suspicious compression ratio.")
        if path.suffix.lower() not in ALLOWED_EXTENSIONS and not path.name.lower().startswith(".env"):
            continue
        try:
            with archive.open(info) as entry:
                content = entry.read(MAX_FILE_BYTES + 1)
            if len(content) > MAX_FILE_BYTES:
                raise RequestError(413, "A ZIP entry exceeds the 2 MiB per-file limit.")
            decoded = content.decode("utf-8-sig")
        except (UnicodeDecodeError, RuntimeError, zipfile.BadZipFile):
            continue
        if "\x00" in decoded:
            continue
        texts.append((raw_name, decoded))
    return texts


def infer_risk(sector: str, users: str, consequential: bool, purpose: str) -> str:
    combined = " ".join((sector, users, purpose)).casefold()
    high_impact = any(
        word in combined
        for word in (
            "recruit", "hiring", "employment", "hr", "credit", "loan", "education",
            "school", "medical", "healthcare", "health care", "biometric", "migration",
            "law enforcement", "policing", "ishga", "kredit", "ta'lim", "tibbiyot",
            "medizin", "einstellung", "kreditvergabe",
        )
    )
    if consequential and high_impact:
        return "potential_high_risk"
    if high_impact:
        return "needs_review"
    if any(word in combined for word in ("chatbot", "chat bot", "deepfake", "synthetic media")):
        return "transparency_review"
    if not purpose.strip() or sector.casefold() in {"other", "unknown", "boshqa", "unbekannt"}:
        return "needs_review"
    return "no_high_risk_signal"


def scan_repository(files: list[tuple[str, str]], scan_id: str) -> list[dict]:
    findings: list[dict] = []
    observed: set[tuple[str, int, str]] = set()

    def add(rule: str, file_path: str, line: int, evidence: str) -> None:
        key = (file_path, line, rule)
        if key in observed or len(findings) >= MAX_FINDINGS:
            return
        observed.add(key)
        findings.append(
            {
                "id": str(uuid.uuid4()),
                "scan_id": scan_id,
                "rule_key": rule,
                "severity": RULES[rule]["severity"],
                "file_path": file_path[:500],
                "line_number": line,
                "evidence": redact(evidence),
                "regulation": RULES[rule]["regulation"],
                "review_status": "open",
                "comment": "",
            }
        )

    for file_path, content in files:
        lines = content.splitlines()
        for line_number, line in enumerate(lines, start=1):
            for pattern in SECRET_PATTERNS:
                if pattern.search(line):
                    add("secret", file_path, line_number, line)
                    break
            if EMAIL_RE.search(line) or IBAN_RE.search(line) or PHONE_RE.search(line):
                add("personal_data", file_path, line_number, line)
            if SOURCE_DATA_RE.search(line):
                add("sensitive_data", file_path, line_number, line)
            if AI_RE.search(line):
                add("ai_dependency", file_path, line_number, line)
            if DATASET_RE.search(line):
                add("dataset_reference", file_path, line_number, line)

    docs_found = any(
        Path(name).name.casefold() in {"readme.md", "model-card.md", "system-description.md"}
        or Path(name).name.casefold().startswith("technical-documentation")
        for name, _ in files
    )
    if files and not docs_found:
        add(
            "missing_docs",
            "(repository)",
            1,
            "No README.md, model-card.md, system-description.md or technical-documentation file was found.",
        )
    return findings


def json_bytes(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False).encode("utf-8")


def safe_row(row: sqlite3.Row) -> dict:
    return dict(row)


def report_html(scan: dict, findings: list[dict], language: str) -> str:
    strings = {
        "en": {
            "title": "Compliance Readiness & Gap Assessment",
            "warning": "Informational screening only. This is not legal advice, a conformity assessment, or a certificate.",
            "summary": "Assessment summary",
            "risk": "Indicative risk screening",
            "purpose": "Intended purpose",
            "sector": "Sector",
            "findings": "Findings",
            "none": "No findings from the enabled checks.",
            "evidence": "Evidence",
            "reference": "Reference for human review",
            "review": "Human review status",
        },
        "de": {
            "title": "Konformitäts-Bereitschaftsbericht",
            "warning": "Nur eine indikative Prüfung. Keine Rechtsberatung, Konformitätsbewertung oder Zertifizierung.",
            "summary": "Zusammenfassung",
            "risk": "Indikative Risikoprüfung",
            "purpose": "Verwendungszweck",
            "sector": "Sektor",
            "findings": "Feststellungen",
            "none": "Keine Feststellungen in den aktivierten Prüfungen.",
            "evidence": "Nachweis",
            "reference": "Rechtsbezug zur menschlichen Prüfung",
            "review": "Prüfstatus",
        },
        "uz": {
            "title": "Muvofiqlikka tayyorgarlik va tafovutlar hisoboti",
            "warning": "Faqat dastlabki skrining. Yuridik maslahat, rasmiy baholash yoki sertifikat emas.",
            "summary": "Baholash xulosasi",
            "risk": "Indikativ xavf skriningi",
            "purpose": "Foydalanish maqsadi",
            "sector": "Soha",
            "findings": "Topilmalar",
            "none": "Yoqilgan tekshiruvlarda topilma aniqlanmadi.",
            "evidence": "Dalil",
            "reference": "Inson tekshiruvi uchun huquqiy havola",
            "review": "Tekshiruv holati",
        },
    }[language]
    cards = []
    for item in findings:
        cards.append(
            "<article class='finding'>"
            f"<h3>{html.escape(item['severity'].upper())} · {html.escape(item['rule_key'].replace('_', ' '))}</h3>"
            f"<p><strong>{html.escape(item['file_path'])}:{item['line_number']}</strong></p>"
            f"<pre>{html.escape(item['evidence'])}</pre>"
            f"<p><strong>{html.escape(strings['reference'])}:</strong> {html.escape(item['regulation'])}</p>"
            f"<p>{html.escape(strings['review'])}: {html.escape(item['review_status'])}</p>"
            "</article>"
        )
    findings_html = "".join(cards) or f"<p>{html.escape(strings['none'])}</p>"
    body = (
        "<!doctype html><html lang='"
        + language
        + "'><meta charset='utf-8'><meta name='viewport' content='width=device-width'>"
        + "<title>"
        + html.escape(strings["title"])
        + "</title><link rel='stylesheet' href='/static/report.css'><script src='/static/report.js' defer></script><body><button id='print-report' class='print-button'>"
        + html.escape({"en": "Print / Save as PDF", "de": "Drucken / Als PDF speichern", "uz": "Chop etish / PDF saqlash"}[language])
        + "</button><h1>"
        + html.escape(strings["title"])
        + "</h1><p>"
        + html.escape(scan["project_name"])
        + " · "
        + html.escape(scan["created_at"])
        + "</p><p class='warning'>"
        + html.escape(strings["warning"])
        + "</p><h2>"
        + html.escape(strings["summary"])
        + "</h2><p><strong>"
        + html.escape(strings["risk"])
        + ":</strong> "
        + html.escape(scan["risk_category"].replace("_", " "))
        + "</p><p><strong>"
        + html.escape(strings["purpose"])
        + ":</strong> "
        + html.escape(scan["purpose"])
        + "</p><p><strong>"
        + html.escape(strings["sector"])
        + ":</strong> "
        + html.escape(scan["sector"])
        + "</p><h2>"
        + html.escape(strings["findings"])
        + "</h2>"
        + findings_html
        + "</body></html>"
    )
    return body


class AppHandler(BaseHTTPRequestHandler):
    server_version = "ReguGuardLocal/1.0"

    def validate_local_request(self, check_origin: bool = False, require_origin: bool = False) -> None:
        host_header = self.headers.get("Host", "")
        try:
            parsed_host = urlparse(f"http://{host_header}")
            allowed_host = parsed_host.hostname in {"127.0.0.1", "localhost", "::1"}
            allowed_port = parsed_host.port == self.server.server_port
        except ValueError:
            allowed_host = False
            allowed_port = False
        if not allowed_host or not allowed_port:
            raise RequestError(421, "Only requests addressed to the local application are accepted.")
        origin = self.headers.get("Origin")
        if check_origin:
            if require_origin and origin is None:
                raise RequestError(403, "An Origin header is required for this state-changing request.")
            if origin is not None and origin.rstrip("/") != f"http://{host_header}".lower():
                raise RequestError(403, "Cross-origin state changes are not allowed.")

    def authenticate(self, require_csrf: bool = False) -> dict:
        cookie = SimpleCookie()
        try:
            cookie.load(self.headers.get("Cookie", ""))
        except Exception:
            raise RequestError(401, "Please sign in.")
        morsel = cookie.get("rg_session")
        if morsel is None:
            raise RequestError(401, "Please sign in.")
        token_hash = hashlib.sha256(morsel.value.encode("ascii", "ignore")).hexdigest()
        with database() as connection:
            row = connection.execute(
                """SELECT s.csrf_token, u.id, u.tenant_id, u.email, u.role, t.name AS tenant_name
                FROM sessions s JOIN app_users u ON u.id=s.user_id
                JOIN tenants t ON t.id=u.tenant_id
                WHERE s.token_hash=? AND s.expires_at>? AND u.active=1""",
                (token_hash, now_iso()),
            ).fetchone()
            if row is None:
                raise RequestError(401, "Your session has expired. Please sign in again.")
            user = dict(row)
        if require_csrf and not secrets.compare_digest(
            self.headers.get("X-CSRF-Token", ""), user["csrf_token"]
        ):
            raise RequestError(403, "The security token is missing or invalid. Reload and try again.")
        return user

    def require_role(self, user: dict, *roles: str) -> None:
        if user["role"] not in roles:
            raise RequestError(403, "Your workspace role does not allow this action.")

    def issue_session(self, user_id: str) -> tuple[str, str]:
        token = secrets.token_urlsafe(32)
        csrf = secrets.token_urlsafe(32)
        current = now_iso()
        expires = (datetime.now(timezone.utc) + timedelta(seconds=SESSION_TTL_SECONDS)).isoformat(timespec="seconds")
        with database() as connection:
            connection.execute("DELETE FROM sessions WHERE expires_at<=?", (current,))
            connection.execute(
                "INSERT INTO sessions (token_hash,user_id,csrf_token,expires_at,created_at) VALUES (?,?,?,?,?)",
                (hashlib.sha256(token.encode()).hexdigest(), user_id, csrf, expires, current),
            )
        return token, csrf

    def set_session_cookie(self, token: str) -> None:
        self.send_header(
            "Set-Cookie",
            f"rg_session={token}; Path=/; HttpOnly; SameSite=Strict; Max-Age={SESSION_TTL_SECONDS}",
        )

    def get_auth_state(self) -> None:
        with database() as connection:
            has_users = connection.execute("SELECT EXISTS(SELECT 1 FROM app_users)").fetchone()[0]
        if not has_users:
            self.send_json(200, {"setup_required": True, "user": None})
            return
        try:
            user = self.authenticate()
        except RequestError as error:
            if error.status == 401:
                self.send_json(200, {"setup_required": False, "user": None})
                return
            raise
        public_user = {key: user[key] for key in ("id", "tenant_id", "email", "role", "tenant_name")}
        self.send_json(200, {"setup_required": False, "user": public_user, "csrf_token": user["csrf_token"]})

    def setup_workspace(self) -> None:
        self.validate_local_request(check_origin=True, require_origin=True)
        payload = self.json_payload(8_192)
        email = str(payload.get("email", "")).strip().casefold()
        password = str(payload.get("password", ""))
        tenant_name = str(payload.get("tenant_name", "")).strip()[:120]
        if not re.fullmatch(r"[^@\s]{1,64}@[^@\s.]+(?:\.[^@\s.]+)+", email) or len(email) > 254:
            raise RequestError(400, "Enter a valid email address.")
        if len(password) < PASSWORD_MIN_LENGTH or len(password) > 256:
            raise RequestError(400, f"Password must contain {PASSWORD_MIN_LENGTH} to 256 characters.")
        if not tenant_name:
            raise RequestError(400, "Workspace name is required.")
        tenant_id, user_id = str(uuid.uuid4()), str(uuid.uuid4())
        with database() as connection:
            connection.execute("BEGIN IMMEDIATE")
            if connection.execute("SELECT EXISTS(SELECT 1 FROM app_users)").fetchone()[0]:
                raise RequestError(409, "Initial setup is already complete.")
            connection.execute(
                "INSERT INTO tenants (id,name,created_at) VALUES (?,?,?)", (tenant_id, tenant_name, now_iso())
            )
            connection.execute(
                "INSERT INTO app_users (id,tenant_id,email,password_hash,role,created_at) VALUES (?,?,?,?,?,?)",
                (user_id, tenant_id, email, password_hash(password), "owner", now_iso()),
            )
            audit(connection, tenant_id, user_id, "workspace_created", tenant_id)
        token, csrf = self.issue_session(user_id)
        self.send_json_with_cookie(201, {"csrf_token": csrf}, token)

    def login(self) -> None:
        self.validate_local_request(check_origin=True, require_origin=True)
        payload = self.json_payload(8_192)
        email = str(payload.get("email", "")).strip().casefold()
        password = str(payload.get("password", ""))
        remote = self.client_address[0]
        rate_key = f"{remote}:{email}"
        with database() as connection:
            row = connection.execute(
                "SELECT id, password_hash FROM app_users WHERE email=? COLLATE NOCASE AND active=1 LIMIT 1", (email,)
            ).fetchone()
        verified = verify_password(password, row["password_hash"] if row is not None else DUMMY_PASSWORD_HASH)
        if not verified:
            limited = register_auth_failure(rate_key)
            if limited:
                raise RequestError(429, "Too many sign-in attempts. Try again in 15 minutes.")
            raise RequestError(401, "Email or password is incorrect.")
        clear_auth_failures(rate_key)
        token, csrf = self.issue_session(row["id"])
        self.send_json_with_cookie(200, {"csrf_token": csrf}, token)

    def logout(self, user: dict) -> None:
        self.validate_local_request(check_origin=True, require_origin=True)
        self.authenticate(require_csrf=True)
        cookie = SimpleCookie()
        cookie.load(self.headers.get("Cookie", ""))
        token = cookie["rg_session"].value
        with database() as connection:
            connection.execute(
                "DELETE FROM sessions WHERE token_hash=?",
                (hashlib.sha256(token.encode()).hexdigest(),),
            )
            audit(connection, user["tenant_id"], user["id"], "logout")
        self.send_response(200)
        self.send_header("Set-Cookie", "rg_session=; Path=/; HttpOnly; SameSite=Strict; Max-Age=0")
        self.send_header("Content-Type", "application/json; charset=utf-8")
        body = json_bytes({"logged_out": True})
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def json_payload(self, limit: int = 8_192) -> dict:
        try:
            payload = json.loads(self.read_body(limit))
        except (json.JSONDecodeError, UnicodeDecodeError):
            raise RequestError(400, "Malformed JSON.")
        if not isinstance(payload, dict):
            raise RequestError(400, "A JSON object is required.")
        return payload

    def send_json_with_cookie(self, status: int, value: object, token: str) -> None:
        body = json_bytes(value)
        self.send_response(status)
        self.set_session_cookie(token)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt: str, *args: object) -> None:
        # Avoid writing request content, query values, or uploaded data to logs.
        super().log_message("%s", fmt.split("%")[0] if not args else "request")

    def end_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_bytes(self, status: int, content: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def send_json(self, status: int, value: object) -> None:
        self.send_bytes(status, json_bytes(value), "application/json; charset=utf-8")

    def read_body(self, limit: int = MAX_UPLOAD_BYTES) -> bytes:
        try:
            size = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            raise RequestError(400, "Invalid Content-Length.")
        if size <= 0 or size > limit:
            raise RequestError(413 if size > limit else 400, "Request body is empty or exceeds the size limit.")
        body = self.rfile.read(size)
        if len(body) != size:
            raise RequestError(400, "Incomplete request body.")
        return body

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        try:
            self.validate_local_request()
            if path == "/":
                self.serve_static(WEB_ROOT / "index.html")
            elif path.startswith("/static/"):
                relative = Path(path.removeprefix("/static/"))
                if relative.is_absolute() or ".." in relative.parts:
                    raise RequestError(404, "Not found.")
                target = (WEB_ROOT / relative).resolve()
                if WEB_ROOT.resolve() not in target.parents:
                    raise RequestError(404, "Not found.")
                self.serve_static(target)
            elif path == "/api/health":
                self.send_json(200, {"status": "ok", "service": "ReguGuard local MVP"})
            elif path == "/api/auth/state":
                self.get_auth_state()
            elif path == "/api/team":
                user = self.authenticate()
                self.require_role(user, "owner", "admin")
                with database() as connection:
                    members = [safe_row(row) for row in connection.execute(
                        "SELECT id,email,role,active,created_at FROM app_users WHERE tenant_id=? ORDER BY created_at",
                        (user["tenant_id"],),
                    )]
                self.send_json(200, {"members": members})
            elif path == "/api/audit":
                user = self.authenticate()
                self.require_role(user, "owner", "admin", "auditor")
                with database() as connection:
                    events = [safe_row(row) for row in connection.execute(
                        """SELECT e.id,e.action,e.target_id,e.created_at,u.email AS actor_email
                        FROM audit_events e JOIN app_users u ON u.id=e.actor_id
                        WHERE e.tenant_id=? ORDER BY e.id DESC LIMIT 200""",
                        (user["tenant_id"],),
                    )]
                self.send_json(200, {"events": events})
            elif path == "/api/audit/verify":
                user = self.authenticate()
                self.require_role(user, "owner", "admin", "auditor")
                with database() as connection:
                    events = connection.execute(
                        """SELECT tenant_id,actor_id,action,target_id,created_at,previous_hash,event_hash
                        FROM audit_events WHERE tenant_id=? ORDER BY id""",
                        (user["tenant_id"],),
                    ).fetchall()
                previous = "GENESIS"
                valid = True
                for event in events:
                    row = dict(event)
                    supplied = row.pop("event_hash")
                    row.pop("tenant_id")
                    row_previous = row.pop("previous_hash")
                    expected = hashlib.sha256(json_bytes({
                        "tenant_id": user["tenant_id"],
                        "actor_id": row["actor_id"],
                        "action": row["action"],
                        "target_id": row["target_id"],
                        "created_at": row["created_at"],
                        "previous_hash": previous,
                    })).hexdigest()
                    if row_previous != previous or supplied != expected:
                        valid = False
                        break
                    previous = supplied
                self.send_json(200, {"valid": valid, "checked_events": len(events)})
            elif path == "/api/scans":
                user = self.authenticate()
                with database() as connection:
                    scans = [safe_row(row) for row in connection.execute(
                        """SELECT id,project_name,risk_category,status,file_count,created_at
                        FROM scans WHERE tenant_id=? ORDER BY created_at DESC LIMIT 100""",
                        (user["tenant_id"],),
                    )]
                    for scan in scans:
                        counts = connection.execute(
                            """SELECT COUNT(*) AS total,
                            SUM(CASE WHEN review_status='open' THEN 1 ELSE 0 END) AS open_count,
                            SUM(CASE WHEN review_status IN ('approved','rejected') THEN 1 ELSE 0 END) AS reviewed_count
                            FROM findings f JOIN scans s ON s.id=f.scan_id
                            WHERE f.scan_id=? AND s.tenant_id=?""", (scan["id"], user["tenant_id"])
                        ).fetchone()
                        scan["finding_count"] = counts["total"] or 0
                        scan["open_count"] = counts["open_count"] or 0
                        scan["reviewed_count"] = counts["reviewed_count"] or 0
                self.send_json(200, {"scans": scans})
            elif path.startswith("/api/scans/"):
                user = self.authenticate()
                parts = path.strip("/").split("/")
                scan_id = parts[2] if len(parts) >= 3 else ""
                if len(parts) == 4 and parts[3] == "report":
                    language = parse_qs(parsed.query).get("lang", ["en"])[0]
                    if language not in {"en", "de", "uz"}:
                        raise RequestError(400, "Unsupported report language.")
                    self.send_report(
                        scan_id, language, user, parse_qs(parsed.query).get("metadata", [""])[0] == "1"
                    )
                elif len(parts) == 3:
                    self.send_scan(scan_id, user)
                else:
                    raise RequestError(404, "Not found.")
            else:
                raise RequestError(404, "Not found.")
        except RequestError as error:
            self.send_json(error.status, {"error": str(error)})
        except (sqlite3.Error, OSError) as error:
            print(f"Request failed: {type(error).__name__}")
            self.send_json(500, {"error": "The request could not be completed."})

    def serve_static(self, target: Path) -> None:
        if not target.is_file():
            raise RequestError(404, "Not found.")
        content_type = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "text/javascript; charset=utf-8",
            ".svg": "image/svg+xml",
        }.get(target.suffix.lower(), "application/octet-stream")
        self.send_bytes(200, target.read_bytes(), content_type)

    def send_scan(self, scan_id: str, user: dict) -> None:
        with database() as connection:
            scan_row = connection.execute(
                "SELECT * FROM scans WHERE id=? AND tenant_id=?", (scan_id, user["tenant_id"])
            ).fetchone()
            if not scan_row:
                raise RequestError(404, "Assessment not found.")
            findings = [safe_row(row) for row in connection.execute(
                """SELECT f.* FROM findings f JOIN scans s ON s.id=f.scan_id
                WHERE f.scan_id=? AND s.tenant_id=?
                ORDER BY CASE f.severity WHEN 'critical' THEN 0 WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, f.file_path, f.line_number""",
                (scan_id, user["tenant_id"]),
            )]
        self.send_json(200, {"scan": safe_row(scan_row), "findings": findings})

    def send_report(self, scan_id: str, language: str, user: dict, metadata_only: bool = False) -> None:
        with database() as connection:
            scan_row = connection.execute(
                "SELECT * FROM scans WHERE id=? AND tenant_id=?", (scan_id, user["tenant_id"])
            ).fetchone()
            if not scan_row:
                raise RequestError(404, "Assessment not found.")
            findings = [safe_row(row) for row in connection.execute(
                """SELECT f.* FROM findings f JOIN scans s ON s.id=f.scan_id
                WHERE f.scan_id=? AND s.tenant_id=? ORDER BY f.file_path,f.line_number""",
                (scan_id, user["tenant_id"]),
            )]
        content = report_html(safe_row(scan_row), findings, language).encode("utf-8")
        digest = hashlib.sha256(content).hexdigest()
        if metadata_only:
            self.send_json(200, {"sha256": digest, "language": language, "format": "printable-html"})
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Content-Disposition", f'inline; filename="reguguard-report-{language}.html"')
        self.send_header("X-Report-SHA256", digest)
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self) -> None:
        path = urlparse(self.path).path
        try:
            if path == "/api/auth/setup":
                self.setup_workspace()
                return
            if path == "/api/auth/login":
                self.login()
                return
            if path == "/api/auth/logout":
                user = self.authenticate(require_csrf=True)
                self.logout(user)
                return
            if path == "/api/team":
                self.validate_local_request(check_origin=True, require_origin=True)
                user = self.authenticate(require_csrf=True)
                self.require_role(user, "owner", "admin")
                payload = self.json_payload()
                email = str(payload.get("email", "")).strip().casefold()
                password = str(payload.get("password", ""))
                role = str(payload.get("role", ""))
                if not re.fullmatch(r"[^@\s]{1,64}@[^@\s.]+(?:\.[^@\s.]+)+", email) or len(email) > 254:
                    raise RequestError(400, "Enter a valid email address.")
                if len(password) < PASSWORD_MIN_LENGTH or len(password) > 256:
                    raise RequestError(400, f"Password must contain {PASSWORD_MIN_LENGTH} to 256 characters.")
                permitted_roles = {"compliance_officer", "developer", "auditor"}
                if user["role"] == "owner":
                    permitted_roles.add("admin")
                if role not in permitted_roles:
                    raise RequestError(400, "This role cannot be assigned by your account.")
                member_id = str(uuid.uuid4())
                with database() as connection:
                    try:
                        connection.execute(
                            "INSERT INTO app_users (id,tenant_id,email,password_hash,role,created_at) VALUES (?,?,?,?,?,?)",
                            (member_id, user["tenant_id"], email, password_hash(password), role, now_iso()),
                        )
                    except sqlite3.IntegrityError:
                        raise RequestError(409, "That email is already a member of this workspace.")
                    audit(connection, user["tenant_id"], user["id"], "member_created", member_id)
                self.send_json(201, {"id": member_id, "email": email, "role": role})
                return
            if path != "/api/scans":
                self.send_json(404, {"error": "Not found."})
                return
            self.validate_local_request(check_origin=True)
            user = self.authenticate(require_csrf=True)
            self.require_role(user, "owner", "admin", "compliance_officer", "developer")
            fields = self.parse_multipart()
            project = fields.get("project_name", "").strip()[:120]
            purpose = fields.get("purpose", "").strip()[:2_000]
            sector = fields.get("sector", "").strip()[:120]
            users = fields.get("users", "").strip()[:500]
            if not project or not purpose or not sector:
                raise RequestError(400, "Project name, intended purpose and sector are required.")
            upload = fields.get("_file")
            if not isinstance(upload, bytes) or not upload:
                raise RequestError(400, "Upload one ZIP file.")
            files = safe_zip_texts(upload)
            if not files:
                raise RequestError(400, "The ZIP contains no supported text files.")
            consequential = fields.get("consequential_decisions", "").casefold() in {"true", "1", "yes", "on"}
            scan_id = str(uuid.uuid4())
            created_at = now_iso()
            findings = scan_repository(files, scan_id)
            risk = infer_risk(sector, users, consequential, purpose)
            with database() as connection:
                connection.execute(
                    """INSERT INTO scans
                    (id, tenant_id, created_by, project_name, purpose, sector, users, consequential_decisions, risk_category, status, file_count, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (scan_id, user["tenant_id"], user["id"], project, purpose, sector, users, int(consequential), risk, "completed", len(files), created_at),
                )
                connection.executemany(
                    """INSERT INTO findings
                    (id, scan_id, rule_key, severity, file_path, line_number, evidence, regulation, review_status, comment)
                    VALUES (:id, :scan_id, :rule_key, :severity, :file_path, :line_number, :evidence, :regulation, :review_status, :comment)""",
                    findings,
                )
                audit(connection, user["tenant_id"], user["id"], "scan_created", scan_id)
            self.send_json(201, {"scan_id": scan_id, "status": "completed", "file_count": len(files), "finding_count": len(findings)})
        except RequestError as error:
            self.send_json(error.status, {"error": str(error)})
        except (sqlite3.Error, OSError, ValueError) as error:
            print(f"Scan failed: {type(error).__name__}")
            self.send_json(500, {"error": "The scan could not be completed. No source files were retained."})

    def parse_multipart(self) -> dict[str, str | bytes]:
        content_type = self.headers.get("Content-Type", "")
        match = re.fullmatch(
            r'multipart/form-data;\s*boundary=(?:"([A-Za-z0-9\'()+_,./:=?-]{1,70})"|([A-Za-z0-9\'()+_,./:=?-]{1,70}))',
            content_type,
            flags=re.IGNORECASE,
        )
        if not match:
            raise RequestError(415, "Expected multipart/form-data.")
        boundary = match.group(1) or match.group(2)
        body = self.read_body()
        message = BytesParser(policy=policy.default).parsebytes(
            f"Content-Type: multipart/form-data; boundary={boundary}\r\nMIME-Version: 1.0\r\n\r\n".encode("ascii") + body
        )
        if not message.is_multipart():
            raise RequestError(400, "Malformed multipart request.")
        fields: dict[str, str | bytes] = {}
        seen_names: set[str] = set()
        for part in message.iter_parts():
            name = part.get_param("name", header="content-disposition")
            if not name or name in seen_names:
                raise RequestError(400, "Missing or duplicate form field.")
            if len(seen_names) >= 20:
                raise RequestError(400, "Too many form fields.")
            seen_names.add(name)
            data = part.get_payload(decode=True) or b""
            filename = part.get_filename()
            if filename is not None:
                if name != "file" or not filename.lower().endswith(".zip"):
                    raise RequestError(400, "Upload a .zip archive using the file field.")
                fields["_file"] = data
            else:
                if len(data) > 4_096:
                    raise RequestError(400, "A form field exceeds the allowed size.")
                charset = (part.get_content_charset() or "utf-8").lower()
                if charset not in {"utf-8", "utf-8-sig", "us-ascii", "iso-8859-1"}:
                    raise RequestError(400, "Unsupported form-field encoding.")
                try:
                    fields[name] = data.decode(charset)
                except UnicodeDecodeError:
                    raise RequestError(400, "Form fields must use a supported text encoding.")
        return fields

    def do_PATCH(self) -> None:
        try:
            self.validate_local_request(check_origin=True, require_origin=True)
            user = self.authenticate(require_csrf=True)
            self.require_role(user, "owner", "admin", "compliance_officer")
        except RequestError as error:
            self.send_json(error.status, {"error": str(error)})
            return
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) != 3 or parts[0] != "api" or parts[1] != "findings":
            self.send_json(404, {"error": "Not found."})
            return
        try:
            payload = self.json_payload()
            status = payload.get("status")
            comment = str(payload.get("comment", ""))[:2_000]
            if status not in {"open", "approved", "rejected"}:
                raise RequestError(400, "Status must be open, approved or rejected.")
            with database() as connection:
                cursor = connection.execute(
                    """UPDATE findings SET review_status=?, comment=? WHERE id=?
                    AND scan_id IN (SELECT id FROM scans WHERE tenant_id=?)""",
                    (status, comment, parts[2], user["tenant_id"]),
                )
                if cursor.rowcount == 0:
                    raise RequestError(404, "Finding not found.")
                scan_id = connection.execute("SELECT scan_id FROM findings WHERE id=?", (parts[2],)).fetchone()["scan_id"]
                audit(connection, user["tenant_id"], user["id"], f"finding_{status}", scan_id)
            self.send_json(200, {"id": parts[2], "review_status": status, "comment": comment})
        except json.JSONDecodeError:
            self.send_json(400, {"error": "Malformed JSON."})
        except RequestError as error:
            self.send_json(error.status, {"error": str(error)})
        except (sqlite3.Error, OSError) as error:
            print(f"Finding update failed: {type(error).__name__}")
            self.send_json(500, {"error": "The review status could not be updated."})

    def do_DELETE(self) -> None:
        try:
            self.validate_local_request(check_origin=True, require_origin=True)
            user = self.authenticate(require_csrf=True)
            self.require_role(user, "owner", "admin", "compliance_officer")
        except RequestError as error:
            self.send_json(error.status, {"error": str(error)})
            return
        parts = urlparse(self.path).path.strip("/").split("/")
        if len(parts) == 3 and parts[:2] == ["api", "team"]:
            self.deactivate_member(parts[2], user)
            return
        if len(parts) != 3 or parts[:2] != ["api", "scans"]:
            self.send_json(404, {"error": "Not found."})
            return
        with database() as connection:
            cursor = connection.execute(
                "DELETE FROM scans WHERE id=? AND tenant_id=?", (parts[2], user["tenant_id"])
            )
            if cursor.rowcount == 0:
                self.send_json(404, {"error": "Assessment not found."})
                return
            audit(connection, user["tenant_id"], user["id"], "scan_deleted", parts[2])
        self.send_json(200, {"deleted": True})

    def deactivate_member(self, member_id: str, user: dict) -> None:
        try:
            self.require_role(user, "owner", "admin")
            with database() as connection:
                member = connection.execute(
                    "SELECT id,role,active FROM app_users WHERE id=? AND tenant_id=?",
                    (member_id, user["tenant_id"]),
                ).fetchone()
                if member is None or not member["active"]:
                    raise RequestError(404, "Workspace member not found.")
                if member_id == user["id"]:
                    raise RequestError(409, "You cannot deactivate your own account.")
                if member["role"] == "owner":
                    raise RequestError(409, "The workspace owner cannot be deactivated.")
                if user["role"] == "admin" and member["role"] == "admin":
                    raise RequestError(403, "An admin cannot deactivate another admin.")
                connection.execute("UPDATE app_users SET active=0 WHERE id=?", (member_id,))
                connection.execute("DELETE FROM sessions WHERE user_id=?", (member_id,))
                audit(connection, user["tenant_id"], user["id"], "member_deactivated", member_id)
            self.send_json(200, {"deactivated": True})
        except RequestError as error:
            self.send_json(error.status, {"error": str(error)})
        except sqlite3.Error as error:
            print(f"Member deactivation failed: {type(error).__name__}")
            self.send_json(500, {"error": "The workspace member could not be deactivated."})


def run() -> None:
    host = os.environ.get("REGUGUARD_HOST", "127.0.0.1")
    port = int(os.environ.get("REGUGUARD_PORT", "8000"))
    if host not in {"127.0.0.1", "localhost", "::1"}:
        if os.environ.get("REGUGUARD_ALLOW_INSECURE_REMOTE") != "yes":
            raise SystemExit("Local-only mode: bind to 127.0.0.1. Remote exposure requires a production security review.")
        raise SystemExit("Remote hosting is not implemented. This local MVP must not be exposed to a network.")
    initialise_database()
    server = ThreadingHTTPServer((host, port), AppHandler)
    print(f"ReguGuard local MVP: http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping ReguGuard.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run()
