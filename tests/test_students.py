import requests
import allure
import pytest

from db_utils import get_db_connection

@pytest.mark.parametrize(
    "age, expected_code",
    [
        (0, 400),
        (1, 200),
        (50, 200),
        (100, 200),
        (101, 400),
    ]
)
def test_add_student_age(
    student_api,
    db_connection,
    age,
    expected_code
):
    student_id = None

    try:
        response = student_api.add_student(
    f"测试学生{age}",
    age
)

        result = response.json()

        print(
            f"\n年龄={age}，实际返回={result}"
        )

        assert result["code"] == expected_code

        if expected_code == 200:
            student_id = result["data"]["id"]

    finally:
        if student_id is not None:
            cursor = db_connection.cursor()

            deleted = cursor.execute(
                "DELETE FROM students WHERE id = %s",
                (student_id,)
            )

            db_connection.commit()

            cursor.close()

            print(
               f"清理测试学生：id={student_id}，"
               f"删除行数={deleted}"
            )

@pytest.mark.parametrize(
    "age, expected_code",
    [
        (0, 400),
        (1, 200),
        (50, 200),
        (100, 200),
        (101, 400),
    ]
)
def test_update_student(
    student_api,
    db_student,
    db_connection,
    age,
    expected_code
):
    student_id = db_student["id"]

    response = student_api.update_student(
    student_id,
    age
)
    result = response.json()

    print(
        f"\n学生ID={student_id}，"
        f"年龄={age}，"
        f"实际返回={result}"
    )

    assert result["code"] == expected_code

    # 只有修改成功时，才验证数据库
    if expected_code == 200:
        cursor = db_connection.cursor()

        try:
            cursor.execute(
                "SELECT id, name, age FROM students WHERE id = %s",
                (student_id,)
            )

            row = cursor.fetchone()

            print("修改后的数据库数据：", row)

            assert row is not None
            assert row[0] == student_id
            assert row[1] == "数据库验证学生"
            assert row[2] == age

        finally:
            cursor.close()

def test_get_students_with_session(student_api):

    response = student_api.get_students()

    result = response.json()

    print("\nSession 查询结果：", result, "feature分支")

    assert result["code"] == 200

def test_add_student_with_session(
    student_api,
    db_connection
):
    response = student_api.add_student(
    "Session测试学生",
    25
)

    result = response.json()

    print("\nSession POST 返回：", result)

    assert result["code"] == 200

    student_id = result["data"]["id"]

    cursor = db_connection.cursor()

    try:
        cursor.execute(
            "SELECT id, name, age FROM students WHERE id = %s",
            (student_id,)
        )

        row = cursor.fetchone()

        print("数据库数据：", row)

        assert row == (
            student_id,
            "Session测试学生",
            25
        )

    finally:
        cursor.execute(
            "DELETE FROM students WHERE id = %s",
            (student_id,)
        )

        db_connection.commit()
        cursor.close()

def test_add_then_get_student(
    student_api,
    db_connection
):
    student_id = None

    try:
        # 第一步：新增学生
        add_response = student_api.add_student(
            "接口关联学生",
            25
        )

        add_result = add_response.json()

        print("\n新增接口返回：", add_result)

        assert add_result["code"] == 200

        student_id = add_result["data"]["id"]

        # 第二步：根据返回的 ID 查询
        get_response = student_api.get_student(student_id)

        get_result = get_response.json()

        print("查询接口返回：", get_result)

        assert get_result["code"] == 200
        assert get_result["data"]["id"] == student_id
        assert get_result["data"]["name"] == "接口关联学生"
        assert get_result["data"]["age"] == 25

    finally:
        if student_id is not None:
            cursor = db_connection.cursor()

            cursor.execute(
                "DELETE FROM students WHERE id = %s",
                (student_id,)
            )

            db_connection.commit()
            cursor.close()

            print("清理接口关联测试学生：", student_id)


def test_student_crud_flow(
    student_api,
    db_connection
):
    student_id = None

    try:
        # 1. 新增学生
        add_response = student_api.add_student(
            "CRUD测试学生",
            18
        )

        add_result = add_response.json()

        print("\n新增返回：", add_result)

        assert add_result["code"] == 200

        student_id = add_result["data"]["id"]

        # 2. 查询新增的学生
        get_response = student_api.get_student(
            student_id
        )

        get_result = get_response.json()

        print("新增后查询：", get_result)

        assert get_result["code"] == 200
        assert get_result["data"]["id"] == student_id
        assert get_result["data"]["name"] == "CRUD测试学生"
        assert get_result["data"]["age"] == 18

        # 3. 修改年龄
        update_response = student_api.update_student(
            student_id,
            25
        )

        update_result = update_response.json()

        print("修改返回：", update_result)

        assert update_result["code"] == 200
        assert update_result["data"]["age"] == 25

        # 4. 再次查询，确认修改成功
        get_response = student_api.get_student(
            student_id
        )

        get_result = get_response.json()

        print("修改后查询：", get_result)

        assert get_result["code"] == 200
        assert get_result["data"]["age"] == 25

        # 5. 查询数据库
        cursor = db_connection.cursor()

        cursor.execute(
            "SELECT id, name, age FROM students WHERE id = %s",
            (student_id,)
        )

        row = cursor.fetchone()

        print("数据库数据：", row)

        assert row == (
            student_id,
            "CRUD测试学生",
            25
        )

        cursor.close()

        # 6. 删除学生
        delete_response = student_api.delete_student(
            student_id
        )

        delete_result = delete_response.json()

        print("删除返回：", delete_result)

        assert delete_result["code"] == 200

        # 7. 删除后再次查询
        get_response = student_api.get_student(
            student_id
        )

        get_result = get_response.json()

        print("删除后查询：", get_result)

        assert get_result["code"] == 404

    finally:
        # 防止测试中途失败导致数据残留
        if student_id is not None:
            cursor = db_connection.cursor()

            cursor.execute(
                "DELETE FROM students WHERE id = %s",
                (student_id,)
            )

            db_connection.commit()

            cursor.close()

            print("最终清理学生：", student_id)