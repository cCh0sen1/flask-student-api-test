# Python 接口自动化测试项目

## 项目介绍

这是一个基于 Python 的接口自动化测试项目，以 Flask 学生管理服务和 MySQL 数据库为测试对象。使用 requests 发起请求、pytest 组织测试及 fixture、Allure 生成测试报告，并通过 GitHub Actions 自动执行测试。项目包含接口响应断言、数据库结果校验和测试数据清理。

## 技术栈

- Python 3.12
- Flask
- pytest
- requests
- Allure（`allure-pytest` 插件；本地查看 HTML 报告需另装 Allure 命令行工具）
- MySQL / PyMySQL
- GitHub Actions

## 项目功能

- 登录接口测试：验证成功登录以及用户名、密码异常场景。
- Token 鉴权测试：验证受保护接口的访问结果。
- 学生模块 CRUD 测试：覆盖新增、查询、修改、删除及年龄边界值。
- 数据库一致性验证：对比接口返回与 MySQL 查询结果，并清理测试数据。
- 参数化测试：使用 pytest 对不同输入和预期结果批量验证。
- 公共测试支持：通过 fixture 管理登录 Token、requests Session、API 封装和数据库连接；`common/logger.py` 提供统一日志入口。

## 项目结构

```text
python_review/
├── .github/workflows/test.yml  # GitHub Actions 测试流程
├── api/                        # 学生接口请求封装
├── app/                        # 用户系统示例，供单元测试使用
├── common/logger.py            # 公共日志工具
├── docs/PROJECT_CONTEXT.md     # 项目背景与缺陷记录
├── server/app.py               # Flask 接口服务
├── sql/init.sql                # MySQL 表结构初始化
├── tests/                      # 接口和用户系统测试
├── test_*.py                   # 根目录的 pytest 示例测试
├── config.py                   # API 地址配置
├── conftest.py                 # pytest fixture
├── db_utils.py                 # 测试侧 MySQL 连接工具
├── db_test.py                  # 独立数据库连接检查脚本
├── pytest.ini                  # 测试发现配置
├── requirements.txt
└── README.md
```

`pytest.ini` 会同时收集根目录的 `test_*.py` 和 `tests/` 中的用例。`report/`、虚拟环境和缓存由 `.gitignore` 忽略。

## 测试运行方式

准备 Python 3.12 和 MySQL 8.0；示例配置使用本机 `127.0.0.1:3306`、数据库 `test_db`、用户 `root`、密码 `king`，API 地址为 `http://127.0.0.1:5000`。本地运行前请确保这些配置与 `config.py`、`db_utils.py` 以及 `server/app.py` 一致。

安装依赖：

```bash
pip install -r requirements.txt
```

初始化数据库：

```bash
mysql -h 127.0.0.1 -uroot -pking -e "CREATE DATABASE IF NOT EXISTS test_db;"
mysql -h 127.0.0.1 -uroot -pking test_db < sql/init.sql
```

第二条命令适用于 Bash 或 Windows `cmd`；在 PowerShell 中可使用 `Get-Content sql/init.sql | mysql -h 127.0.0.1 -uroot -pking test_db`。

先在一个终端启动服务：

```bash
python server/app.py
```

再在项目根目录的另一个终端运行全部测试：

```bash
pytest
```

生成并查看 Allure 报告：

```bash
pytest --alluredir=report
allure serve report
```

`allure-pytest` 已列在 `requirements.txt` 中；`allure serve` 还需要单独安装 Allure 命令行工具。普通 `pytest` 运行无需安装该命令行工具。

## CI/CD

向 `master` 分支推送代码或提交拉取请求时，`.github/workflows/test.yml` 会在 Ubuntu 环境中安装 Python 3.12 和项目依赖，启动 MySQL 8.0、初始化 `test_db`，随后启动 Flask 服务并执行 `pytest`。当前工作流执行测试，但没有上传 Allure HTML 报告。

## 项目亮点

- 使用 requests + pytest 组合接口请求、参数化和断言，覆盖登录、鉴权及学生 CRUD 流程。
- 通过数据库查询核对接口结果，并在 fixture 或测试清理阶段删除创建的数据。
- 将请求封装、fixture、数据库工具与服务端代码分层，便于定位失败原因。
- CI 自动准备数据库和服务后运行同一条 `pytest` 命令，降低本地与 CI 的执行差异。
- 曾通过 Postman 发现学生修改接口只更新年龄、不更新姓名的问题；修复后验证姓名与年龄均正确更新。完整排查过程见[缺陷分析记录](docs/PROJECT_CONTEXT.md)。
