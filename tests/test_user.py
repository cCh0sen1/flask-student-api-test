import pytest

from app.user import UserSystem



@pytest.fixture
def user():

    return UserSystem()



def test_register(user):

    result = user.register(
        "admin",
        "123456"
    )

    assert result == "注册成功"



@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("admin","123456","登录成功"),
        ("admin","111111","密码错误"),
        ("test","123456","用户不存在")
    ]
)
def test_login(
        user,
        username,
        password,
        expected
):

    user.register(
        "admin",
        "123456"
    )

    result = user.login(
        username,
        password
    )

    assert result == expected