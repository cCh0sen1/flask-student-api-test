import pytest


@pytest.fixture
def resource():

    print("准备测试环境")

    yield

    print("清理测试环境")


def test_demo(resource):

    print("执行测试")
