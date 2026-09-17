import requests


def test_baidu():

    response = requests.get(
        "https://www.baidu.com"
    )


    assert response.status_code == 200
