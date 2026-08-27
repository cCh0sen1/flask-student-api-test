import requests

def test_userinfo(base_url, login_token):

    response = requests.get(
        f"{base_url}/userinfo",
        headers={
            "Authorization": f"Bearer {login_token}"
        }
    )

    print(response.json())

    assert response.json()["code"] == 200
    assert response.json()["name"] == "leo"
    assert response.json()["age"] == 18

