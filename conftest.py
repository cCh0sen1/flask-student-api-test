import pytest
import requests

from config import BASE_URL
from db_utils import get_db_connection
from api.student_api import StudentAPI


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def login_token(base_url):
    response = requests.post(
        f"{base_url}/login",
        json={
            "username": "admin",
            "password": "123456"
        }
    )

    return response.json()["token"]

@pytest.fixture(scope="session")
def http_session(base_url):
    session = requests.Session()

    response = session.post(
        f"{base_url}/login",
        json={
            "username": "admin",
            "password": "123456"
        }
    )

    token = response.json()["token"]

    session.headers.update({
        "Authorization": f"Bearer {token}"
    })

    yield session

    session.close()

@pytest.fixture
def student_api(http_session, base_url):
    return StudentAPI(
        http_session,
        base_url
    )


@pytest.fixture
def db_connection():
    connection = get_db_connection()

    yield connection

    connection.close()


@pytest.fixture
def db_student(base_url, login_token):

    response = requests.post(
        f"{base_url}/students",
        headers={
            "Authorization": f"Bearer {login_token}"
        },
        json={
            "name": "数据库验证学生",
            "age": 23
        }
    )

    student = response.json()["data"]

    print("\n创建数据库测试学生：", student)

    yield student

    student_id = student["id"]

    requests.delete(
        f"{base_url}/students/{student_id}",
        headers={
            "Authorization": f"Bearer {login_token}"
        }
    )

    print("清理数据库测试学生：", student_id)
    
    return response.json()["data"]