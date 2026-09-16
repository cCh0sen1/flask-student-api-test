import requests


def test_login_userinfo(base_url):

    # 登录
    login_url = f"{base_url}/login"

    login_data = {
        "username": "admin",
        "password": "123456"
    }

    login_response = requests.post(
        login_url,
        json=login_data
    )

    login_json = login_response.json()


    # 判断登录是否成功
    assert login_json["code"] == 200


    # 获取token
    token = login_json["token"]


    # 查询用户信息
    userinfo_url = f"{base_url}/userinfo"

    headers = {
        "Authorization": f"Bearer {token}"
    }


    userinfo_response = requests.get(
        userinfo_url,
        headers=headers
    )


    userinfo_json = userinfo_response.json()


    # 判断用户信息接口
    assert userinfo_json["code"] == 200
    assert userinfo_json["name"] == "leo"
