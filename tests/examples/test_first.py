def test_login_success():

    # 模拟登录返回结果
    result = "登录成功"

    # 验证结果
    assert result == "登录成功"


def test_login_fail():

    # 模拟错误密码
    result = "密码错误"

    # 验证
    assert result == "密码错误"
