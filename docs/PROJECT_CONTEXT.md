# 项目介绍

本项目是一个面向测试开发方向的 Flask 学生管理 API 自动化测试项目。项目以本地 Flask 服务和 MySQL 数据库为测试对象，先通过 Postman 完成功能验证和缺陷定位，再使用 requests、pytest 与 Allure 建立可复用的接口自动化测试框架，并结合数据库查询验证接口操作结果。

# 技术栈

- Python
- Flask
- requests
- pytest
- Allure
- MySQL
- Git

# 当前项目结构

- `server/`：Flask API 服务，包含登录、用户信息以及学生增删改查接口，并通过 PyMySQL 访问 MySQL。
- `api/`：接口二次封装层；`student_api.py` 中的 `StudentAPI` 统一封装学生 CRUD 请求，测试用例通过该层调用接口。
- `tests/`：pytest 测试用例，覆盖登录、Token 鉴权、用户信息和学生 CRUD 等场景。
- `conftest.py`：集中管理 pytest fixture，包括服务地址、登录 Token、requests Session、API Client、数据库连接和学生测试数据清理。
- `config.py`：保存测试环境基础配置，目前主要维护本地 API 的 `BASE_URL`。
- `db_utils.py`：封装 MySQL 数据库连接，为接口结果校验和测试数据清理提供支持。
- `tests/examples/`：保留 pytest fixture、scope、yield 和参数化基础示例。
- `report/`：保存 Allure 测试结果数据和相关附件。
- `README.md`：项目说明及已发现接口缺陷的修复记录。

# 已完成内容

- 登录接口测试
- Token 鉴权测试
- pytest 参数化测试
- Allure 标记及结果数据生成
- fixture 集中管理
- requests Session 封装及鉴权请求头复用
- API 层二次封装
- 学生 CRUD 自动化测试
- 数据库连接、接口结果校验和测试数据清理

# 最近一次问题与修复记录

使用 Postman 测试 `PUT /students/<student_id>` 时，请求体为：

```json
{
  "name": "LLL",
  "age": 28
}
```

接口返回修改成功，但实际仅 `age` 更新，`name` 仍保持原值。通过对比 Postman 请求、接口响应和后端 `update_student` 实现，确认接口原本只读取 `age`，SQL 也只执行：

```sql
UPDATE students SET age = %s WHERE id = %s
```

修复后，后端会同时读取并更新 `name` 和 `age`，成功响应返回最新学生数据。使用 Postman 回归验证后，学生 `84` 的 `name` 更新为 `LLL`、`age` 更新为 `28`，两个字段均正常生效。

# 当前自动化测试状态

目前接口测试覆盖：

- `login`
- `user/userinfo`
- `students` CRUD

当前测试框架已经包含 fixture 管理、Token 管理、requests Session、API 封装和数据库验证能力。学生相关测试能够串联接口请求与数据库查询，并在测试结束后清理创建的测试数据。

# 当前工程状态与可选优化

项目现已接入 Jenkins Pipeline 和 GitHub Actions。Jenkins 使用 Docker Compose 构建隔离的 MySQL、Flask 与 pytest 环境，发布 JUnit 报告并在结束后清理资源；GitHub Actions 作为推送和 Pull Request 的轻量验证通道。

后续可按需要完善 API Client 的公共请求处理、Allure HTML 报告的 CI 展示，以及测试数据之间的隔离。
