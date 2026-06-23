# Prompt 记录

## 使用工具

- 工具：Codex
- 模型：codex5.5
- 仓库：SuYK-666/CocoWeb
- 工作目录：`成员代码/苏禹宽_GithubProjectAnalyzer`

## 关键 Prompt 1：项目背景与工作边界

```text
背景说明：
我正在完成信息安全管理课程的 AI 辅助开发实践作业。当前项目是 GitHub Project Analyzer，一个基于 Flask 的本地 Web 工具。用户提交 DeepSeek API Key、GitHub 仓库地址和分析方向后，系统异步生成 Markdown、HTML、DOCX 三种分析报告。

任务范围：
请只在 成员代码/苏禹宽_GithubProjectAnalyzer 目录内进行代码修改和文件新增。作业要求中的 docs/、reports/、测试文件和期末报告都必须放在该个人目录内，不能修改其他成员目录或仓库根目录中的无关文件。

目标：
选择一个与信息安全直接相关的功能点进行实质性补强，要求功能可以运行，并能通过测试或验证证明确实解决了安全问题。优先选择涉及访问控制、输入处理、权限判断、数据读取或错误响应的模块。

交付物：
1. 完成安全功能代码实现；
2. 增加必要的测试或验证脚本；
3. 在个人目录下补充 docs/risk-analysis.md、docs/constraint-doc.md、docs/prompt-records.md、docs/security-checklist.md、docs/fix-report.md；
4. 在个人目录下补充 reports/scan-report.md 和 reports/before-after-diff.md；
5. 在个人目录下生成 期末报告_苏禹宽.md，详细记录风险识别、Prompt、安全代码片段、偏差修正和验证结果。
```

## 关键 Prompt 2：安全功能实现约束

```text
请对 Web 分析任务结果访问流程进行安全加固。

风险背景：
当前系统通过 job_id 查询任务状态、读取 SSE 日志和下载报告。job_id 是资源定位标识，如果它同时作为访问凭据，一旦泄露，第三方可能直接读取分析日志和报告产物。

要求：
1. 每个分析任务创建时生成独立 access token；
2. job_id 只用于定位任务，不能作为唯一访问凭据；
3. /api/result/<job_id> 必须校验 access token；
4. /api/stream/<job_id> 必须校验 access token；
5. /api/download/<job_id>/<fmt> 必须校验 access token；
6. 缺少 token 时返回 401；
7. token 错误时返回 403；
8. token 必须使用安全随机数生成，不能由时间戳、仓库名、用户名或递增序列拼接得到；
9. token 比较必须使用常量时间比较；
10. 前端需要自动携带 token，保证合法用户仍能查看进度、轮询状态和下载报告；
11. 前端不得把任务 access token 写入 localStorage；
12. 不得记录或提交真实 DeepSeek API Key、GitHub Token 或其他敏感凭据。

测试要求：
请新增单元测试，至少覆盖以下场景：
1. 不带 token 访问任务结果应被拒绝；
2. 使用错误 token 访问任务结果应被拒绝；
3. 使用正确 token 访问任务结果应成功；
4. 下载接口必须先执行授权检查。
```

## 关键 Prompt 3：安全审查与整改要求

```text
请对刚才生成的代码进行安全审查，重点检查：
1. 安全约束是否落实在实际代码逻辑中，而不只是写在注释或文档中；
2. 三个敏感接口 result、stream、download 是否都调用了同一套授权校验；
3. token 是否使用 secrets 等安全随机源生成；
4. token 比较是否使用常量时间比较；
5. 前端是否只在当前运行状态中保存任务 token，而不是写入 localStorage；
6. 下载链接、SSE 链接、轮询链接是否都能携带 token；
7. 新增测试是否能证明未授权访问被拒绝、合法访问仍可用。

如果发现偏差，请记录问题是什么、如何修正、修正后应满足什么条件，并把结果写入 docs/fix-report.md、reports/before-after-diff.md 和 期末报告_苏禹宽.md。
```

## AI 生成结果中与安全约束相关的关键片段

```python
access_token = secrets.token_urlsafe(32)
```

```python
if not expected_token or not provided_token:
    abort(401, description="missing job access token")
if not secrets.compare_digest(expected_token, provided_token):
    abort(403, description="invalid job access token")
```

```javascript
response = await fetch(withQuery(state.resultUrl, { t: Date.now(), token: state.accessToken }), {
    cache: "no-store",
    headers: { "Cache-Control": "no-cache" },
});
```

## 偏差与修正记录

- 下载链接需要同步携带 token，否则新授权校验会拦截合法用户下载。已在 `downloadUrls` 中追加 `?token=...`。
- 轮询 URL 已包含 token 后，不能再简单拼接 `?t=...`。已新增 `withQuery` 统一合并查询参数。
- 单元测试第一次运行时，环境中的第三方 `tests` 包抢占了导入路径，导致 `tests.test_job_access_control` 无法导入。已新增本地 `tests/__init__.py` 固定测试包解析。

