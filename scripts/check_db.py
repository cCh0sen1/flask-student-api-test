"""Manual MySQL connectivity check for the test environment."""

import os

import pymysql


connection = pymysql.connect(
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3307")),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "king"),
    database=os.getenv("DB_NAME", "test_db"),
    charset="utf8mb4",
)

print("MySQL 连接成功")
connection.close()
