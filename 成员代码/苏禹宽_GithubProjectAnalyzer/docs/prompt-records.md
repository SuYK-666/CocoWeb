# Prompt 记录

## 使用工具

- 工具：Codex
- 模型：codex5.5
- 仓库：SuYK-666/CocoWeb
- 工作目录：`成员代码/苏禹宽_GithubProjectAnalyzer`

## 关键 Prompt 1：任务启动约束

```text
这是我们的小组作业，然后我 fork 了 SuYK-666/CocoWeb。
请按照期末作业文档要求，只在 /成员代码/苏禹宽_GithubProjectAnalyzer 内补强代码。
所有新增 docs、reports 等目录也必须放在该个人目录下。
选取一个具体安全功能并真正落实，最后生成 期末报告_苏禹宽.md。
完成后提交到我的 GitHub fork，并向 AndrewAccuracy/CocoWeb main 发起新的 PR，不要覆盖已有 PR，不要 merge。
```

## 关键 Prompt 2：安全约束转化

```text
请基于风险识别结果实现一个真实安全功能：
为 Web 分析任务增加访问控制。
要求：
1. 每个任务创建时生成独立访问 token；
2. job_id 仅用于定位任务，不能作为访问凭据；
3. /api/result、/api/stream、/api/download 必须校验 token；
4. 缺失 token 返回 401，错误 token 返回 403；
5. token 使用安全随机数生成，比较使用常量时间比较；
6. 前端自动携带 token，但不要保存到 localStorage；
7. 增加单元测试覆盖无 token、错 token、正确 token。
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

- 初次改动后下载链接需要同步携带 token，否则新授权校验会拦截合法用户下载。已在 `downloadUrls` 中追加 `?token=...`。
- 单元测试第一次运行时，环境中的第三方 `tests` 包抢占了导入路径，导致 `tests.test_job_access_control` 无法导入。已新增本地 `tests/__init__.py` 固定测试包解析。

