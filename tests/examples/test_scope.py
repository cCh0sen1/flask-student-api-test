import pytest


@pytest.fixture(scope="function")
def func_fixture():

    print("function fixture")


@pytest.fixture(scope="session")
def session_fixture():

    print("session fixture")


def test_one(func_fixture, session_fixture):

    print("执行测试1")


def test_two(func_fixture, session_fixture):

    print("执行测试2")
