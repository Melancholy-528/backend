import uuid
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_auth_flow_signup_login_me():
    # 1. Signup with unique email
    email = f"test.entrepreneur.{uuid.uuid4().hex[:8]}@sih.gov.in"
    signup_payload = {
        "full_name": "Kavita Devi",
        "email": email,
        "password": "mysecretpassword",
        "phone": "9123456780",
        "category": "SC",
        "state": "Uttar Pradesh",
        "district": "Varanasi",
        "annual_income": 120000,
    }
    signup_res = client.post("/auth/signup", json=signup_payload)
    assert signup_res.status_code == 200
    signup_data = signup_res.json()
    assert "access_token" in signup_data
    assert signup_data["token_type"] == "bearer"
    assert signup_data["user"]["email"] == email
    assert signup_data["user"]["category"] == "SC"

    token = signup_data["access_token"]

    # 2. Duplicate signup fails with 400
    dup_res = client.post("/auth/signup", json=signup_payload)
    assert dup_res.status_code == 400

    # 3. Login with correct credentials
    login_res = client.post("/auth/login", json={
        "email": email,
        "password": "mysecretpassword",
    })
    assert login_res.status_code == 200
    assert "access_token" in login_res.json()

    # 4. Login with invalid password fails with 401
    bad_login = client.post("/auth/login", json={
        "email": email,
        "password": "wrongpassword",
    })
    assert bad_login.status_code == 401

    # 5. Get current user profile with JWT token
    me_res = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    me_data = me_res.json()
    assert me_data["full_name"] == "Kavita Devi"
    assert me_data["district"] == "Varanasi"

    # 6. Access /auth/me without token fails with 401
    no_auth_res = client.get("/auth/me")
    assert no_auth_res.status_code == 401

    # 7. Update profile
    update_res = client.put("/auth/me", json={
        "annual_income": 150000,
        "category": "Women"
    }, headers={"Authorization": f"Bearer {token}"})
    assert update_res.status_code == 200
    assert update_res.json()["annual_income"] == 150000
    assert update_res.json()["category"] == "Women"

    # 8. Bookmark a scheme
    save_res = client.post("/users/saved-schemes/PMEGP", headers={"Authorization": f"Bearer {token}"})
    assert save_res.status_code == 200
    assert "PMEGP" in save_res.json()["saved_schemes"]

    # 9. Get saved schemes details
    saved_schemes_res = client.get("/users/saved-schemes", headers={"Authorization": f"Bearer {token}"})
    assert saved_schemes_res.status_code == 200
    saved_list = saved_schemes_res.json()
    assert len(saved_list) >= 1
    assert any(s["scheme_code"] == "PMEGP" for s in saved_list)

    # 10. Unbookmark scheme
    del_res = client.delete("/users/saved-schemes/PMEGP", headers={"Authorization": f"Bearer {token}"})
    assert del_res.status_code == 200
    assert "PMEGP" not in del_res.json()["saved_schemes"]
