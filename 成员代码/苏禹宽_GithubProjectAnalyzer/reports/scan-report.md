# 扫描与验证报告

## 扫描范围

- `webapp.py`
- `web/static/app.js`
- `tests/test_job_access_control.py`

## 执行命令

```powershell
python -m compileall webapp.py web\static\app.js tests
python -m unittest tests.test_job_access_control -v
```

## 结果摘要

```text
compileall：通过
unittest：Ran 4 tests in 0.024s，OK
```

## 测试覆盖点

- `test_result_requires_access_token`：缺少 token 时 `/api/result/<job_id>` 返回 401。
- `test_result_rejects_invalid_access_token`：错误 token 时返回 403。
- `test_result_accepts_valid_access_token`：正确 token 时返回 200，并返回任务状态。
- `test_download_requires_access_token_before_status_check`：下载接口先校验授权，缺少 token 返回 401。

## 残余风险

- 当前任务状态保存在进程内存中，服务重启后任务丢失；这属于原架构限制，不属于本次访问控制功能范围。
- token 通过查询参数传给 SSE 和下载链接，便于浏览器原生能力使用；生产环境建议配合 HTTPS、短期任务过期和服务端会话进一步强化。

