import pymysql


def get_db_connection():

    return pymysql.connect(
        host="127.0.0.1",
        port=3307,
        user="root",
        password="king",
        database="test_db",
        charset="utf8mb4"
    )