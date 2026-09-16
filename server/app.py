import pymysql
import os
from flask import Flask, request, jsonify

app = Flask(__name__)


# =========================
# MySQL 数据库连接
# =========================
def get_db_connection():

    return pymysql.connect(
        host=os.getenv("DB_HOST", "127.0.0.1"),
        port=int(os.getenv("DB_PORT", 3306)),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", "king"),
        database=os.getenv("DB_NAME", "test_db"),
        charset="utf8mb4"
    )


# =========================
# 登录接口
# =========================
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data["username"]
    password = data["password"]

    print(f"收到请求：{username} {password}")

    # 用户不存在
    if username != "admin":
        return jsonify({
            "code": 404,
            "msg": "用户不存在"
        })

    # 密码错误
    if password != "123456":
        return jsonify({
            "code": 401,
            "msg": "密码错误"
        })

    # 登录成功
    return jsonify({
        "code": 200,
        "msg": "我是雷宇涵大王",
        "token": "abcdef123456"
    })


# =========================
# 用户信息接口
# =========================
@app.route("/userinfo", methods=["GET"])
def userinfo():
    token = request.headers.get("Authorization")

    if token != "Bearer abcdef123456":
        return jsonify({
            "code": 401,
            "msg": "未登录"
        })

    return jsonify({
        "code": 200,
        "name": "leo",
        "age": 18
    })


# =========================
# 查询学生
# =========================
@app.route("/students", methods=["GET"])
def get_students():
    token = request.headers.get("Authorization")

    if token != "Bearer abcdef123456":
        return jsonify({
            "code": 401,
            "msg": "未登录"
        })

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, age FROM students"
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    data = []

    for row in rows:
        data.append({
            "id": row[0],
            "name": row[1],
            "age": row[2]
        })

    return jsonify({
        "code": 200,
        "data": data
    })


# =========================
# 新增学生
# =========================
@app.route("/students", methods=["POST"])
def add_student():
    token = request.headers.get("Authorization")

    if token != "Bearer abcdef123456":
        return jsonify({
            "code": 401,
            "msg": "未登录"
        })

    data = request.json

    name = data["name"]
    age = data["age"]
    if age < 1 or age > 100:
        return jsonify({
            "code": 400,
            "msg": "年龄必须在1到100之间"
        })

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO students (name, age)
        VALUES (%s, %s)
        """,
        (name, age)
    )

    connection.commit()

    student_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "code": 200,
        "msg": "新增成功",
        "data": {
            "id": student_id,
            "name": name,
            "age": age
        }
    })

# =========================
# 修改学生年龄
# =========================
@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    token = request.headers.get("Authorization")

    if token != "Bearer abcdef123456":
        return jsonify({
            "code": 401,
            "msg": "未登录"
        })

    data = request.json
    name = data["name"]
    age = data["age"]

    # 年龄校验
    if age < 1 or age > 100:
        return jsonify({
            "code": 400,
            "msg": "年龄必须在1到100之间"
        })

    connection = get_db_connection()
    cursor = connection.cursor()

    # 先确认学生是否存在
    cursor.execute(
        "SELECT id, name, age FROM students WHERE id = %s",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        cursor.close()
        connection.close()

        return jsonify({
            "code": 404,
            "msg": "学生不存在"
        })

    # 修改姓名和年龄
    cursor.execute(
        "UPDATE students SET name = %s, age = %s WHERE id = %s",
        (name, age, student_id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "code": 200,
        "msg": "修改成功",
        "data": {
            "id": student[0],
            "name": name,
            "age": age
        }
    })

# =========================
# 查询单个学生
# =========================
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student(student_id):
    token = request.headers.get("Authorization")

    if token != "Bearer abcdef123456":
        return jsonify({
            "code": 401,
            "msg": "未登录"
        })

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, age FROM students WHERE id = %s",
        (student_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        return jsonify({
            "code": 404,
            "msg": "学生不存在"
        })

    return jsonify({
        "code": 200,
        "data": {
            "id": row[0],
            "name": row[1],
            "age": row[2]
        }
    })

# =========================
# 删除学生
# =========================
@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    token = request.headers.get("Authorization")

    if token != "Bearer abcdef123456":
        return jsonify({
            "code": 401,
            "msg": "未登录"
        })

    connection = get_db_connection()
    cursor = connection.cursor()

    # 先查询学生是否存在
    cursor.execute(
        "SELECT id FROM students WHERE id = %s",
        (student_id,)
    )

    student = cursor.fetchone()

    if student is None:
        cursor.close()
        connection.close()

        return jsonify({
            "code": 404,
            "msg": "学生不存在"
        })

    # 删除学生
    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (student_id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "code": 200,
        "msg": "删除成功"
    })


# =========================
# 启动 Flask
# =========================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
