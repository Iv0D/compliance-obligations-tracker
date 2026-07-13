import logging

from fastapi.testclient import TestClient

_TAX_ID = "123456789"


def _create(client: TestClient, **overrides) -> dict:
    payload = {
        "type": "annual_report",
        "title": "Annual report",
        "owner": "Ana",
        "due_date": "2026-12-01",
        "company_tax_id": _TAX_ID,
        "requires_document": False,
    }
    payload.update(overrides)
    response = client.post("/obligations", json=payload)
    assert response.status_code == 201, response.text
    return response.json()


def test_create_masks_tax_id_and_never_exposes_raw(client: TestClient) -> None:
    body = _create(client)

    assert body["company_tax_id_masked"] == "••••6789"
    assert "company_tax_id" not in body
    assert body["status"] == "pending"
    assert body["version"] == 1


def test_get_missing_returns_404(client: TestClient) -> None:
    response = client.get("/obligations/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_change_status_rejects_invalid_transition(client: TestClient) -> None:
    obligation = _create(client)

    response = client.patch(
        f"/obligations/{obligation['id']}/status",
        json={"status": "submitted", "version": 1},
    )

    assert response.status_code == 422
    assert response.json()["error"]["code"] == "invalid_transition"


def test_change_status_happy_path_increments_version_and_audits(
    client: TestClient,
) -> None:
    obligation = _create(client)

    response = client.patch(
        f"/obligations/{obligation['id']}/status",
        json={"status": "in_progress", "version": 1},
    )

    assert response.status_code == 200, response.text
    assert response.json()["version"] == 2

    detail = client.get(f"/obligations/{obligation['id']}").json()
    assert len(detail["audit_events"]) == 1
    assert detail["audit_events"][0]["from_status"] == "pending"
    assert detail["audit_events"][0]["to_status"] == "in_progress"


def test_doc_gated_blocks_submit_until_document_attached(client: TestClient) -> None:
    obligation = _create(client, requires_document=True)
    oid = obligation["id"]
    client.patch(f"/obligations/{oid}/status", json={"status": "in_progress", "version": 1})

    blocked = client.patch(
        f"/obligations/{oid}/status", json={"status": "submitted", "version": 2}
    )
    assert blocked.status_code == 422
    assert blocked.json()["error"]["code"] == "document_required"

    attached = client.post(
        f"/obligations/{oid}/documents",
        json={"filename": "f.pdf", "mock_url": "http://x/f.pdf"},
    )
    assert attached.status_code == 201

    submitted = client.patch(
        f"/obligations/{oid}/status", json={"status": "submitted", "version": 2}
    )
    assert submitted.status_code == 200, submitted.text


def test_change_status_stale_version_conflicts(client: TestClient) -> None:
    obligation = _create(client)
    oid = obligation["id"]
    client.patch(f"/obligations/{oid}/status", json={"status": "in_progress", "version": 1})

    conflict = client.patch(
        f"/obligations/{oid}/status", json={"status": "submitted", "version": 1}
    )

    assert conflict.status_code == 409
    assert conflict.json()["error"]["code"] == "conflict"


def test_soft_delete_hides_obligation(client: TestClient) -> None:
    obligation = _create(client)
    oid = obligation["id"]

    assert client.delete(f"/obligations/{oid}").status_code == 204
    assert client.get(f"/obligations/{oid}").status_code == 404
    assert client.get("/obligations").json() == []
    assert client.delete(f"/obligations/{oid}").status_code == 404


def test_change_status_does_not_log_raw_tax_id(
    client: TestClient, caplog
) -> None:
    obligation = _create(client)

    with caplog.at_level(logging.INFO):
        client.patch(
            f"/obligations/{obligation['id']}/status",
            json={"status": "in_progress", "version": 1},
        )

    assert "status_changed" in caplog.text
    assert _TAX_ID not in caplog.text
