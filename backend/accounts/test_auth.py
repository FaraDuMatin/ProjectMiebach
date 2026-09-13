def test_login_then_me(client, django_user_model):
    django_user_model.objects.create_user(username="tester", password="secret123")
    response = client.post("/api/auth/login/", {"username": "tester", "password": "secret123"}, content_type="application/json")
    assert response.status_code == 200
    assert client.get("/api/auth/me/").json() == {"username": "tester"}


def test_wrong_password(client, django_user_model):
    django_user_model.objects.create_user(username="tester", password="secret123")
    response = client.post("/api/auth/login/", {"username": "tester", "password": "nope"}, content_type="application/json")
    assert response.status_code == 400
