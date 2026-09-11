# Flask 学生管理接口测试项目

## 接口测试缺陷发现与修复记录

- 测试接口：`PUT /students/<student_id>`
- 测试工具：Postman
- 问题现象：请求体同时传入 `name` 和 `age` 后，接口返回“修改成功”，但查询结果显示仅 `age` 更新，`name` 仍为原值。
- 问题定位：对比 Postman 请求、接口响应及后端实现后，确认 `update_student` 只读取 `data["age"]`，SQL 也只更新 `age`，导致 `name` 被忽略。
- 修复内容：补充 `name` 字段读取，将 SQL 调整为同时更新 `name` 和 `age`，并在成功响应中返回更新后的学生信息。
- 验证结果：使用 Postman 对学生 `84` 回归测试，响应返回 `name` 为 `LLL`、`age` 为 `28`，两个字段均已正常更新，缺陷修复验证通过。
