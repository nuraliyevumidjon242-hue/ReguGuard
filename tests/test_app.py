import hashlib
import http.client
import io
import json
import stat
import sqlite3
import tempfile
import threading
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

import app


def make_zip(entries: dict[str, str]) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, content in entries.items():
            archive.writestr(name, content)
    return buffer.getvalue()


class AnalysisTests(unittest.TestCase):
    def test_context_controls_indicative_risk(self):
        self.assertEqual(
            app.infer_risk("hr", "recruiters", True, "Ranks job applicants"),
            "potential_high_risk",
        )
        self.assertEqual(
            app.infer_risk("hr", "recruiters", False, "Ranks job applicants"),
            "needs_review",
        )
        self.assertEqual(
            app.infer_risk("general", "developers", False, "Formats source code"),
            "no_high_risk_signal",
        )
        self.assertEqual(app.infer_risk("other", "", False, ""), "needs_review")

    def test_finds_and_redacts_secrets_and_personal_data(self):
        source = make_zip({
            "README.md": "# Project\n",
            "src/app.py": (
                'API_KEY = "synthetic-token-123456789"\n'
                'contact = "alice@example.test"\n'
                "model = langchain\n"
                "dataset = patient_data\n"
            ),
        })
        findings = app.scan_repository(app.safe_zip_texts(source), "scan-id")
        by_rule = {finding["rule_key"]: finding for finding in findings}
        self.assertIn("secret", by_rule)
        self.assertIn("personal_data", by_rule)
        self.assertIn("ai_dependency", by_rule)
        self.assertIn("dataset_reference", by_rule)
        self.assertNotIn("synthetic-token", by_rule["secret"]["evidence"])
        self.assertNotIn("alice@example.test", by_rule["personal_data"]["evidence"])

    def test_rejects_traversal_and_large_entries(self):
        traversal = make_zip({"../outside.py": "print('no')"})
        with self.assertRaises(app.RequestError):
            app.safe_zip_texts(traversal)
        large = make_zip({"oversized.py": "x" * (app.MAX_FILE_BYTES + 10)})
        with self.assertRaises(app.RequestError) as error:
            app.safe_zip_texts(large)
        self.assertEqual(error.exception.status, 413)

    def test_rejects_symlinks_and_compression_bombs(self):
        symlink_buffer = io.BytesIO()
        link = zipfile.ZipInfo("linked.py")
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        with zipfile.ZipFile(symlink_buffer, "w") as archive:
            archive.writestr(link, "../outside.py")
        with self.assertRaises(app.RequestError):
            app.safe_zip_texts(symlink_buffer.getvalue())

        compressed_bomb = make_zip({"source.py": "0" * 1_200_000})
        with self.assertRaises(app.RequestError) as error:
            app.safe_zip_texts(compressed_bomb)
        self.assertEqual(error.exception.status, 413)

    def test_report_escapes_untrusted_content(self):
        scan = {
            "project_name": "<script>alert(1)</script>",
            "created_at": "2026-01-01",
            "risk_category": "needs_review",
            "purpose": "<img src=x>",
            "sector": "other",
        }
        rendered = app.report_html(scan, [], "en")
        self.assertNotIn("<script>", rendered)
        self.assertNotIn("<img src=x>", rendered)
        self.assertIn("&lt;script&gt;", rendered)


class DatabaseMigrationTests(unittest.TestCase):
    def test_existing_duplicate_emails_fail_with_actionable_migration_error(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            data_dir = Path(temp_dir)
            db_path = data_dir / "legacy.sqlite3"
            with patch.object(app, "DATA_DIR", data_dir), patch.object(app, "DB_PATH", db_path):
                with app.database() as connection:
                    connection.executescript(
                        """
                        CREATE TABLE tenants (id TEXT PRIMARY KEY, name TEXT NOT NULL, created_at TEXT NOT NULL);
                        CREATE TABLE app_users (
                            id TEXT PRIMARY KEY, tenant_id TEXT NOT NULL, email TEXT NOT NULL,
                            password_hash TEXT NOT NULL, role TEXT NOT NULL, created_at TEXT NOT NULL,
                            UNIQUE(tenant_id, email)
                        );
                        INSERT INTO tenants VALUES ('tenant-a', 'A', '2026-01-01');
                        INSERT INTO tenants VALUES ('tenant-b', 'B', '2026-01-01');
                        INSERT INTO app_users VALUES ('user-a', 'tenant-a', 'Owner@example.test', 'hash', 'owner', '2026-01-01');
                        INSERT INTO app_users VALUES ('user-b', 'tenant-b', 'owner@example.test', 'hash', 'owner', '2026-01-01');
                        """
                    )

                with self.assertRaisesRegex(RuntimeError, "duplicate accounts exist"):
                    app.initialise_database()


class HttpWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_patch = patch.object(app, "DATA_DIR", Path(self.temp_dir.name))
        self.db_patch = patch.object(app, "DB_PATH", Path(self.temp_dir.name) / "test.sqlite3")
        self.data_patch.start()
        self.db_patch.start()
        self.addCleanup(self.data_patch.stop)
        self.addCleanup(self.db_patch.stop)
        app.initialise_database()
        self.server = app.ThreadingHTTPServer(("127.0.0.1", 0), app.AppHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.cookie = ""
        self.csrf = ""
        status, headers, response = self.request(
            "POST",
            "/api/auth/setup",
            json.dumps({
                "tenant_name": "Primary workspace",
                "email": "owner@example.test",
                "password": "test-password-12",
            }),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 201, response)
        normalized = {key.lower(): value for key, value in headers.items()}
        self.cookie = normalized["set-cookie"].split(";", 1)[0]
        self.csrf = json.loads(response)["csrf_token"]
        self.addCleanup(self.close_server)
        self.addCleanup(self.temp_dir.cleanup)

    def close_server(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=3)

    def request(self, method, path, body=None, headers=None):
        connection = http.client.HTTPConnection(*self.server.server_address, timeout=5)
        request_headers = {}
        if self.cookie:
            request_headers["Cookie"] = self.cookie
        if self.csrf:
            request_headers["X-CSRF-Token"] = self.csrf
        if method.upper() in {"POST", "PATCH", "DELETE", "PUT"}:
            request_headers["Origin"] = f"http://127.0.0.1:{self.server.server_port}"
        request_headers.update(headers or {})
        connection.request(method, path, body=body, headers=request_headers)
        response = connection.getresponse()
        payload = response.read()
        result_headers = dict(response.getheaders())
        connection.close()
        return response.status, result_headers, payload

    def test_scan_review_report_and_delete_flow(self):
        boundary = "test-reguguard-boundary"
        archive = make_zip({
            "README.md": "# Example\n",
            "service.py": 'api_key = "synthetic-token-123456789"\n',
        })
        fields = {
            "project_name": b"Sample project",
            "sector": b"general",
            "users": b"Developers",
            "purpose": b"Local code review",
            "consequential_decisions": b"false",
        }
        body = bytearray()
        for name, value in fields.items():
            body.extend(f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"\r\n\r\n".encode())
            body.extend(value + b"\r\n")
        body.extend(
            f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"sample.zip\"\r\nContent-Type: application/zip\r\n\r\n".encode()
        )
        body.extend(archive + b"\r\n")
        body.extend(f"--{boundary}--\r\n".encode())
        status, _, response = self.request(
            "POST", "/api/scans", bytes(body),
            {"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        self.assertEqual(status, 201, response)
        scan_result = json.loads(response)
        scan_id = scan_result["scan_id"]
        self.assertGreaterEqual(scan_result["finding_count"], 1)

        status, _, response = self.request("GET", f"/api/scans/{scan_id}")
        self.assertEqual(status, 200)
        result = json.loads(response)
        finding = next(item for item in result["findings"] if item["rule_key"] == "secret")

        status, _, response = self.request(
            "PATCH",
            f"/api/findings/{finding['id']}",
            json.dumps({"status": "approved", "comment": "Reviewed"}),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 200, response)
        self.assertEqual(json.loads(response)["review_status"], "approved")

        status, headers, report = self.request("GET", f"/api/scans/{scan_id}/report?lang=de")
        self.assertEqual(status, 200)
        normalized_headers = {key.lower(): value for key, value in headers.items()}
        self.assertEqual(normalized_headers["x-report-sha256"], hashlib.sha256(report).hexdigest())
        self.assertIn("Konformitäts-Bereitschaftsbericht".encode(), report)

        status, _, metadata = self.request(
            "GET", f"/api/scans/{scan_id}/report?lang=de&metadata=1"
        )
        self.assertEqual(status, 200)
        report_metadata = json.loads(metadata)
        self.assertEqual(report_metadata["sha256"], normalized_headers["x-report-sha256"])
        self.assertEqual(report_metadata["format"], "printable-html")

        status, _, response = self.request("DELETE", f"/api/scans/{scan_id}")
        self.assertEqual(status, 200, response)
        status, _, _ = self.request("GET", f"/api/scans/{scan_id}")
        self.assertEqual(status, 404)
        status, _, response = self.request("GET", "/api/audit/verify")
        self.assertEqual(status, 200, response)
        self.assertTrue(json.loads(response)["valid"])

    def test_static_page_has_security_headers(self):
        status, headers, payload = self.request("GET", "/")
        self.assertEqual(status, 200)
        self.assertIn("default-src 'self'", headers["Content-Security-Policy"])
        self.assertIn(b"ReguGuard", payload)

    def test_rejects_cross_origin_state_changes_and_host_rebinding(self):
        status, _, _ = self.request(
            "PATCH",
            "/api/findings/not-a-real-id",
            json.dumps({"status": "approved"}),
            {"Content-Type": "application/json", "Origin": "http://attacker.example"},
        )
        self.assertEqual(status, 403)
        status, _, _ = self.request(
            "GET",
            "/api/health",
            headers={"Host": "attacker.example"},
        )
        self.assertEqual(status, 421)

    def test_tenant_isolation_and_csrf_enforcement(self):
        other_tenant, other_user, other_scan = "tenant-other", "user-other", "scan-other"
        with app.database() as connection:
            connection.execute(
                "INSERT INTO tenants (id,name,created_at) VALUES (?,?,?)",
                (other_tenant, "Other workspace", app.now_iso()),
            )
            connection.execute(
                "INSERT INTO app_users (id,tenant_id,email,password_hash,role,created_at) VALUES (?,?,?,?,?,?)",
                (other_user, other_tenant, "other@example.test", app.password_hash("other-password-123"), "owner", app.now_iso()),
            )
            connection.execute(
                """INSERT INTO scans
                (id,tenant_id,created_by,project_name,purpose,sector,users,consequential_decisions,risk_category,status,file_count,created_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (other_scan, other_tenant, other_user, "Secret workspace", "Purpose", "other", "", 0, "needs_review", "completed", 1, app.now_iso()),
            )
        status, _, _ = self.request("GET", f"/api/scans/{other_scan}")
        self.assertEqual(status, 404)
        status, _, response = self.request("GET", "/api/scans")
        self.assertNotIn(b"Secret workspace", response)
        status, _, _ = self.request(
            "PATCH",
            "/api/findings/no-such-finding",
            json.dumps({"status": "approved"}),
            {"X-CSRF-Token": ""},
        )
        self.assertEqual(status, 403)

    def test_initial_setup_is_one_time_and_login_issues_session(self):
        status, _, _ = self.request(
            "POST",
            "/api/auth/setup",
            json.dumps({
                "tenant_name": "Attacker workspace",
                "email": "attacker@example.test",
                "password": "another-password-123",
            }),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 409)
        status, headers, response = self.request(
            "POST",
            "/api/auth/login",
            json.dumps({"email": "owner@example.test", "password": "test-password-12"}),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 200, response)
        normalized = {key.lower(): value for key, value in headers.items()}
        self.assertIn("rg_session=", normalized["set-cookie"])
        self.assertTrue(json.loads(response)["csrf_token"])

    def test_role_permissions_and_member_session_revocation(self):
        status, _, response = self.request(
            "POST",
            "/api/team",
            json.dumps({
                "email": "developer@example.test",
                "password": "developer-password-12",
                "role": "developer",
            }),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 201, response)
        member_id = json.loads(response)["id"]

        owner_cookie, owner_csrf = self.cookie, self.csrf
        status, headers, response = self.request(
            "POST",
            "/api/auth/login",
            json.dumps({"email": "developer@example.test", "password": "developer-password-12"}),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 200, response)
        normalized = {key.lower(): value for key, value in headers.items()}
        member_cookie = normalized["set-cookie"].split(";", 1)[0]
        member_csrf = json.loads(response)["csrf_token"]

        self.cookie, self.csrf = member_cookie, member_csrf
        status, _, _ = self.request("GET", "/api/scans")
        self.assertEqual(status, 200)
        status, _, _ = self.request(
            "POST",
            "/api/team",
            json.dumps({
                "email": "unauthorized@example.test",
                "password": "another-password-12",
                "role": "developer",
            }),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 403)

        self.cookie, self.csrf = owner_cookie, owner_csrf
        status, _, response = self.request("DELETE", f"/api/team/{member_id}")
        self.assertEqual(status, 200, response)
        status, _, response = self.request("GET", "/api/team")
        members = json.loads(response)["members"]
        self.assertFalse(next(member for member in members if member["id"] == member_id)["active"])

        self.cookie, self.csrf = member_cookie, member_csrf
        status, _, _ = self.request("GET", "/api/scans")
        self.assertEqual(status, 401)
        status, _, _ = self.request(
            "POST",
            "/api/auth/login",
            json.dumps({"email": "developer@example.test", "password": "developer-password-12"}),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 401)

    def test_admin_cannot_deactivate_owner_or_another_admin(self):
        admin_ids = []
        for email in ("admin-one@example.test", "admin-two@example.test"):
            status, _, response = self.request(
                "POST",
                "/api/team",
                json.dumps({"email": email, "password": "admin-password-123", "role": "admin"}),
                {"Content-Type": "application/json"},
            )
            self.assertEqual(status, 201, response)
            admin_ids.append(json.loads(response)["id"])

        owner_cookie, owner_csrf = self.cookie, self.csrf
        status, headers, response = self.request(
            "POST",
            "/api/auth/login",
            json.dumps({"email": "admin-one@example.test", "password": "admin-password-123"}),
            {"Content-Type": "application/json"},
        )
        self.assertEqual(status, 200, response)
        normalized = {key.lower(): value for key, value in headers.items()}
        self.cookie = normalized["set-cookie"].split(";", 1)[0]
        self.csrf = json.loads(response)["csrf_token"]

        status, _, response = self.request("DELETE", f"/api/team/{admin_ids[1]}")
        self.assertEqual(status, 403, response)
        with app.database() as connection:
            owner_id = connection.execute(
                "SELECT id FROM app_users WHERE email='owner@example.test'"
            ).fetchone()["id"]
        status, _, response = self.request("DELETE", f"/api/team/{owner_id}")
        self.assertEqual(status, 409, response)
        status, _, response = self.request("DELETE", f"/api/team/{admin_ids[0]}")
        self.assertEqual(status, 409, response)

        self.cookie, self.csrf = owner_cookie, owner_csrf
        status, _, response = self.request("DELETE", f"/api/team/{admin_ids[0]}")
        self.assertEqual(status, 200, response)
        status, _, response = self.request("DELETE", f"/api/team/{admin_ids[0]}")
        self.assertEqual(status, 404, response)

    def test_global_email_uniqueness_is_case_insensitive(self):
        with app.database() as connection:
            connection.execute(
                "INSERT INTO tenants (id,name,created_at) VALUES (?,?,?)",
                ("other-tenant", "Other workspace", app.now_iso()),
            )
            with self.assertRaises(sqlite3.IntegrityError):
                connection.execute(
                    """INSERT INTO app_users (id,tenant_id,email,password_hash,role,created_at)
                    VALUES (?,?,?,?,?,?)""",
                    ("other-owner", "other-tenant", "OWNER@example.test",
                     app.password_hash("other-password-123"), "owner", app.now_iso()),
                )

    def test_audit_hash_chain_detects_tampering(self):
        with app.database() as connection:
            event = connection.execute("SELECT id FROM audit_events ORDER BY id LIMIT 1").fetchone()
            connection.execute("DROP TRIGGER audit_events_no_update")
            connection.execute("UPDATE audit_events SET event_hash='tampered' WHERE id=?", (event["id"],))
        status, _, response = self.request("GET", "/api/audit/verify")
        self.assertEqual(status, 200)
        self.assertFalse(json.loads(response)["valid"])


if __name__ == "__main__":
    unittest.main()
