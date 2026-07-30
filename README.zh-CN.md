<p align="center">
  <img src="assets/hero.svg" alt="Embodied Eval Automation" width="100%">
</p>

# 具身评测自动化

[English](README.md)

这是一个面向“模型 + 机器人 benchmark/仿真平台 + 批量 episode”任务的通用 Agent Skill，同时按照当前 Codex 的 skills-only plugin（仅含 skill 的插件）结构打包。

它不提供模型权重或 benchmark 源码，而是让智能体以可恢复、可审计的方式完成：

- 先确认本机与服务器工作目录，再进行任何写入；
- 通过 SSH、云平台命令行、GitHub 或 Hugging Face 的已有认证方式获得最小权限；
- 只读盘点并复用现有仓库、环境、checkpoint、数据集和缓存；
- 固定官方 commit/revision/哈希，并先讲清模型与 benchmark；
- 按单请求、单 episode、小批量、中批量或批准规模逐级验收；
- 保留模型官方原生输出，同时生成可比较的统一表示；
- 对长任务进行远端守护、本地控制、定时复核、断点恢复和磁盘治理；
- 回传后校验 SHA256，只有满足边界与审批条件才清理远端数据；
- 最终交付 manifest、验证报告、可视化、失败清单和复现包。

## 快速使用

可以这样唤醒：

> 使用 `$embodied-eval-automation` 帮我在 `<服务器>` 上运行 `<模型> + <benchmark>` 并生成批量 episode。我还没有确定认证方式。请先确认工作目录、权限、官方版本、现有可复用资产、目标 episode 集合、存储阈值和完成条件；没有得到我批准前，不得下载、安装、上传、删除、启动付费算力或提交 Git。

skill 不会要求用户把密码、令牌、私钥或云凭据粘贴到对话中。密码登录应由用户在交互终端中自行输入；需要无人值守时，skill 会先询问是否允许创建专用 SSH 密钥，并只处理公钥授权。

## 核心阶段

1. `G0`：连接方式、工作目录、权限边界、主机和已有资产只读盘点。
2. `G1`：官方资料、版本与哈希锁定；模型/benchmark 技术报告；资产复用矩阵。
3. `G2–G4`：隔离环境、缺失资源、运行时与渲染验证。
4. `G5`：一次真实模型请求，不运行完整 episode。
5. `G6`：一次真实闭环；同一 rollout 生成官方原生、当前统一、候选统一三种表示。
6. `G7`：跨 task/init 的小批量；分析格式差异并由用户审批，再进入中批量。
7. `G8`：只运行用户批准的规模；远端守护、本地控制器和定时监控共同工作。
8. `G9`：重建索引，审计缺失/重复/损坏，生成可视化和复现交付。

## 数据可比性约束

- `pair_key` 不包含模型身份。
- `T` 个真实 transition 对应 `T+1` 个 observation。
- 每次真实模型请求写入 `policy_queries`。
- 完整原始 action chunk 与实际执行 action 分开保存。
- 世界模型或策略模型预测写在 prediction 区域，不能冒充真实环境 observation。
- 不支持的能力写 capability，采集不完整写 quality flag，不猜测补值。

## 安装

普通 skill 安装只需要：

```text
skills/embodied-eval-automation/
```

仓库根目录还包含 `.codex-plugin/plugin.json`，可作为仅含 skill 的 Codex 插件进行本地测试与后续公开发布。发布前请查看 [发布清单](docs/publishing-checklist.md)。

## 验证

```bash
python skills/embodied-eval-automation/scripts/validate_repository.py .
python -m unittest discover -s tests -v
```

所有验证脚本只使用 Python 标准库。

## 安全边界

安装、下载、上传、产生费用、删除、Git 写入和外部通知是相互独立的授权。远端清理必须在本地下载、哈希校验、归档展开、episode 审计和目标路径边界检查全部通过后进行。

详细规则见 [SECURITY.md](SECURITY.md) 和 [PRIVACY.md](PRIVACY.md)。

## 参与贡献

欢迎补充新的云平台接入方式、benchmark、模型家族、转换器、验证器和故障恢复经验。请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。

## 许可证

MIT，见 [LICENSE](LICENSE)。
