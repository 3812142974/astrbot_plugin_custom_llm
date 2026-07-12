import aiohttp
import json
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.config.astrbot_config import AstrBotConfig

@register("astrbot_plugin_custom_llm", "3812142974", "自定义LLM调用插件", "1.0.0")
class CustomLLMPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    async def initialize(self):
        """插件初始化方法"""
        logger.info("自定义LLM插件已加载")
        logger.info(f"API URL: {self.config.get('api_url', '未配置')}")
        logger.info(f"模型名称: {self.config.get('model_name', '未配置')}")
        logger.info(f"触发指令: /{self.config.get('command_name', 'ask')}")

    # 【修改点1】：使用 on_message 拦截所有消息，以便动态读取配置中的指令名
    @filter.on_message
    async def handle_custom_llm(self, event: AstrMessageEvent):
        """
        自定义LLM调用指令
        用法: /<指令名> 你的问题内容
        """
        # 获取配置
        api_url = self.config.get("api_url", "").strip()
        api_key = self.config.get("api_key", "").strip()
        model_name = self.config.get("model_name", "").strip()
        command_name = self.config.get("command_name", "ask").strip()

        # 获取用户消息
        message_str = event.message_str.strip()

        # 【修改点2】：动态匹配指令名 (兼容带 / 和不带 / 的情况)
        user_question = None
        if message_str.startswith(f"/{command_name}"):
            user_question = message_str[len(f"/{command_name}"):].strip()
        elif message_str.startswith(command_name):
            user_question = message_str[len(command_name):].strip()
            
        # 如果不是触发的指令，直接 return，不拦截消息，交给其他插件或默认大模型
        if user_question is None:
            return

        # 检查配置是否完整
        if not api_url:
            yield event.plain_result("❌ 错误：未配置 API URL，请在插件配置中填写以 /v1 结尾的 API 地址")
            return
        if not api_key:
            yield event.plain_result("❌ 错误：未配置 API Key，请在插件配置中填写")
            return
        if not model_name:
            yield event.plain_result("❌ 错误：未配置模型名称，请在插件配置中填写")
            return

        if not user_question:
            yield event.plain_result(f"❌ 请输入要问的内容，例如：/{command_name} 你好")
            return

        # 发送提示消息
        yield event.plain_result(f"🤔 正在调用模型 {model_name} 处理你的问题...")

        # 构建 API 请求
        base_url = api_url.rstrip("/")
        if base_url.endswith("/v1"):
            chat_url = f"{base_url}/chat/completions"
        else:
            chat_url = f"{base_url}/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": model_name,
            "messages": [
                {
                    "role": "user",
                    "content": user_question
                }
            ],
            "stream": False
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    chat_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        if "choices" in result and len(result["choices"]) > 0:
                            content = result["choices"][0]["message"]["content"]
                            yield event.plain_result(f"✅ 模型回复：\n\n{content}")
                        else:
                            logger.error(f"API 响应格式异常: {result}")
                            yield event.plain_result(f"❌ API 响应格式异常：{json.dumps(result, ensure_ascii=False)[:500]}")
                    else:
                        error_text = await response.text()
                        logger.error(f"API 请求失败，状态码: {response.status}, 响应: {error_text}")
                        yield event.plain_result(f"❌ API 请求失败，状态码: {response.status}\n错误信息: {error_text[:500]}")
        except aiohttp.ClientError as e:
            logger.error(f"网络请求错误: {e}")
            yield event.plain_result(f"❌ 网络请求错误: {str(e)}")
        except Exception as e:
            logger.error(f"未捕获的异常: {e}")
            yield event.plain_result(f"❌ 发生错误: {str(e)}")

    async def terminate(self):
        """插件销毁方法"""
        logger.info("自定义LLM插件已卸载")