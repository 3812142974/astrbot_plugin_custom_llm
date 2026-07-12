# AstrBot 插件：自定义 LLM 调用 (Custom LLM Caller)

一个用于绕过 AstrBot 默认大模型处理流，直接通过指定指令调用特定 OpenAI 兼容 API 的轻量级插件。

## ✨ 功能特性

- 🚀 **独立调用**：通过特定指令触发，直接请求指定的 LLM API，**不经过 AstrBot 的默认模型和 Prompt 处理**。
- ⚙️ **高度可配**：支持自定义 API 地址、API Key 和模型名称。
- 🔌 **广泛兼容**：支持所有兼容 OpenAI `/v1/chat/completions` 接口格式的平台（如 DeepSeek、OpenAI、硅基流动、通义千问、Moonshot 等）。
- 🛠️ **自定义指令**：可自定义触发指令名称（默认 `/ask`），避免与其他插件冲突。
- 📦 **协议无关**：基于 AstrBot 核心事件系统开发，完美兼容 **NapCat**、Lagrange、LLOneBot 等主流消息平台适配器。

---

## 📦 安装方法

### 方法一：手动安装（推荐）
1. 下载或克隆本仓库的代码。
2. 将包含 `main.py`、`metadata.yaml` 和 `_conf_schema.json` 的文件夹重命名为 `astrbot_plugin_custom_llm`。
3. 将该文件夹放入 AstrBot 的插件目录中（通常为 `AstrBot/data/plugins/`）。
4. 在 AstrBot WebUI 的「插件管理」页面，点击「重载插件」或重启 AstrBot。

### 方法二：通过 Git 安装
如果你的 AstrBot 环境支持直接拉取 Git 仓库，可以在插件目录执行：
```bash
cd data/plugins
git clone https://github.com/3812142974/astrbot_plugin_custom_llm.git
```

---

## ⚙️ 配置说明

安装并加载插件后，请在 AstrBot WebUI 的 **「插件配置」 -> 「astrbot_plugin_custom_llm」** 中进行以下配置：

| 配置项 | 说明 | 示例 / 默认值 |
| :--- | :--- | :--- |
| **api_url** | API 平台的基础地址，**必须以 `/v1` 结尾**。 | `https://api.deepseek.com/v1`<br>`https://api.openai.com/v1` |
| **api_key** | 你的 API 密钥 (Token)。 | `sk-xxxxxxxxxxxxxxxx` |
| **model_name** | 需要调用的具体模型名称。 | `deepseek-chat`<br>`gpt-4o`<br>`qwen-turbo` |
| **command_name** | 触发此插件的指令名称（无需加 `/`）。 | `ask` (默认)<br>`llm`<br>`chat` |

> 💡 **提示**：配置修改后，通常无需重启，插件会自动读取最新配置。

---

## 📖 使用方法

在 QQ（或其他接入平台）中，向机器人发送以下格式的消息：

```text
/<指令名> <你要问的问题>
```

### 示例

假设你配置的指令名为默认的 `ask`：

**用户发送：**
> /ask 请用简短的语言解释一下什么是量子纠缠。

**机器人回复：**
> 🤔 正在调用模型 deepseek-chat 处理你的问题...
> 
> ✅ 模型回复：
> 
> 量子纠缠是一种量子力学现象，指两个或多个粒子在相互作用后，由于各个粒子所拥有的特性已综合成为整体性质，无法单独描述各个粒子的性质，只能描述整体系统的性质。当对其中一个粒子进行测量时，会瞬间影响另一个粒子的状态，无论它们相距多远。

---

## ❓ 常见问题 (FAQ)

**Q1: 提示“未配置 API URL”或“API 请求失败”怎么办？**
- 请检查 WebUI 中的插件配置是否已正确填写并保存。
- 确认 `api_url` 是否严格以 `/v1` 结尾（例如 `https://api.example.com/v1`，而不是 `https://api.example.com`）。
- 检查 `api_key` 是否有效且余额充足。

**Q2: 为什么回复速度很慢或者超时？**
- 插件默认设置了 60 秒的请求超时时间。如果模型思考时间较长或网络不佳，可能会超时。
- 如果你使用的是海外 API（如 OpenAI），请确保运行 AstrBot 的服务器/电脑已经配置了正确的网络代理。

**Q3: 这个插件会影响机器人正常的聊天（默认模型）吗？**
- **完全不会**。只有当你发送以 `/ask`（或你自定义的指令）开头的消息时，才会触发此插件。其他普通消息依然会走 AstrBot 的默认大模型处理流程。

**Q4: 支持流式输出（打字机效果）吗？**
- 当前版本为一次性返回完整回复，不支持流式输出。如果需要流式输出，可以在 `main.py` 中将 `stream` 参数改为 `True` 并修改相应的解析逻辑。

---

## 🛠️ 开发说明

本项目基于 [AstrBot](https://github.com/Soulter/AstrBot) 官方插件模板开发。
- AstrBot 版本测试环境：`v4.x` (兼容 2.26.0+ 核心逻辑)
- 消息适配器：NapCat / Lagrange / LLOneBot

## 📄 开源协议

MIT License. 自由使用、修改和分发。