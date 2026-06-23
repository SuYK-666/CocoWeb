# 安全审查清单

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| 是否实现真实功能而非仅修改 README | 通过 | 新增任务访问令牌校验，影响后端接口和前端调用。 |
| 是否涉及身份认证、权限判断或数据存取 | 通过 | 对任务日志、结果和下载产物增加授权判断。 |
| 是否避免把 `job_id` 当作唯一凭据 | 通过 | 新增 `access_token`，`job_id` 仅定位任务。 |
| 令牌是否安全生成 | 通过 | 使用 `secrets.token_urlsafe(32)`。 |
| 令牌比较是否避免普通字符串比较 | 通过 | 使用 `secrets.compare_digest`。 |
| 结果查询是否受保护 | 通过 | `/api/result/<job_id>` 调用 `_authorize_job`。 |
| 实时日志是否受保护 | 通过 | `/api/stream/<job_id>` 调用 `_authorize_job`。 |
| 报告下载是否受保护 | 通过 | `/api/download/<job_id>/<fmt>` 调用 `_authorize_job`。 |
| 前端是否保存任务 token 到 localStorage | 通过 | 仅保存在运行期 `state.accessToken`。 |
| 是否新增验证测试 | 通过 | `tests/test_job_access_control.py` 覆盖 4 个授权场景。 |
| 是否泄露真实 API Key/GitHub Token | 通过 | 文档与测试均使用占位内容，未写入真实密钥。 |

