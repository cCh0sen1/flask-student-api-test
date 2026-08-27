import pytest
import requests
import allure

@allure.feature("登录模块")
@allure.title("登录接口测试")
@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("admin", "123456", 200),
        ("admin", "111111", 401),
        ("test", "123456", 404)
    ]
)
def test_login(base_url, username, password, expected):

    with allure.step("① 发送登录请求"):
        response = requests.post(
            f"{base_url}/login",
            json={
                "username": username,
                "password": password
            }
        )

    with allure.step("② 校验返回状态码"):
        assert response.json()["code"] == expected

    if expected == 200:
        with allure.step("③ 获取 Token"):
            print("Token:", response.json()["token"])