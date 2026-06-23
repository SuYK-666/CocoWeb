# 整改说明与验证记录

## 问题是什么

原 Web 任务接口只要知道 `job_id` 即可查询结果、读取实时日志、下载报告。`job_id` 同时承担资源定位与访问授权职责，一旦出现在浏览器历史、错误日志或聊天记录中，就可能造成分析报告泄露。

## 怎么改

- 在 `_create_job` 中为每个任务生成 `access_token`。
- 新增 `_get_request_token`，支持从 `Authorization: Bearer` 或查询参数 `token` 读取令牌。
- 新增 `_authorize_job`，统一完成任务存在性、令牌缺失和令牌错误判断。
- 在 `/api/stream/<job_id>`、`/api/result/<job_id>`、`/api/download/<job_id>/<fmt>` 中调用 `_authorize_job`。
- 前端在创建任务成功后保存本次会话的 `accessToken`，轮询、SSE 和下载链接均携带该 token。
- 新增单元测试覆盖缺失 token、错误 token、正确 token 和下载接口授权前置检查。

## 改完应满足什么条件

- 未携带 token 访问任务结果时返回 401。
- 携带错误 token 访问任务结果时返回 403。
- 携带正确 token 时可以读取任务状态。
- 下载接口在任务状态检查前先执行授权，避免未授权请求探测产物状态。

## 验证结果

```text
python -m compileall webapp.py web\static\app.js tests
结果：通过

python -m unittest tests.test_job_access_control -v
结果：4 项测试全部通过
```

