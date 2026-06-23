# 整改前后对比说明

## 整改前

- 创建任务后返回 `jobId`、`streamUrl`、`resultUrl` 和 `downloadBaseUrl`。
- `/api/result/<job_id>` 不校验访问者身份。
- `/api/stream/<job_id>` 不校验访问者身份。
- `/api/download/<job_id>/<fmt>` 不校验访问者身份。
- 前端轮询时直接请求 `resultUrl?t=...`。

## 整改后

- 创建任务时同时生成 `accessToken`。
- `streamUrl`、`resultUrl` 和下载链接均携带当前任务 token。
- 三类任务读取接口统一调用 `_authorize_job`。
- 缺少 token 返回 401，错误 token 返回 403。
- 单元测试验证授权行为。

## 安全效果

整改后，即使攻击者知道或获取了 `job_id`，也不能直接读取日志、结果或下载报告；必须同时持有该任务创建时返回的访问 token。

