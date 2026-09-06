from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig
import astrbot.api.message_components as Comp
import aiohttp

API_URL = "https://hw233.cn/api/RandomImg.php"


@register(
    "astrbot_plugin_hw",
    "H_W , Grok",
    "自用插件",
    "1.0.0",
)
class HWPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    def _is_allowed(self, event: AstrMessageEvent) -> bool:
        """检查当前会话是否允许使用指令。
        白名单为空：全部开放（群聊 + 私聊）。
        白名单非空：仅白名单内的群号可使用；私聊直接拒绝。
        """
        whitelist = self.config.get("group_whitelist") or []
        # 统一转成字符串，避免类型不一致
        whitelist = [str(g).strip() for g in whitelist if str(g).strip()]

        if not whitelist:
            return True

        group_id = event.get_group_id()
        if not group_id:
            # 私聊且开启了白名单 -> 不允许
            return False

        return str(group_id) in whitelist

    @filter.command("hw", alias={"HW"})
    async def hw(self, event: AstrMessageEvent):
        """随机获取一张 OC 图片"""
        if not self._is_allowed(event):
            # 静默忽略，不回复任何内容
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(API_URL, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                    if resp.status != 200:
                        logger.error(f"[astrbot_plugin_hw] API 返回状态码: {resp.status}")
                        yield event.plain_result("获取图片失败，请稍后再试~")
                        return
                    data = await resp.json()

            url = data.get("url")
            if not url:
                logger.error(f"[astrbot_plugin_hw] API 返回数据缺少 url: {data}")
                yield event.plain_result("获取图片失败，请稍后再试~")
                return

            time_str = data.get("time", "")
            by = data.get("by", "")
            oc_id = data.get("id", "")

            # 格式：日期 by 作者\nID xxx
            text = f"{time_str} by {by}\nID {oc_id}"

            chain = [
                Comp.Image.fromURL(url),
                Comp.Plain(text),
            ]
            yield event.chain_result(chain)

        except aiohttp.ClientError as e:
            logger.error(f"[astrbot_plugin_hw] 网络请求失败: {e}")
            yield event.plain_result("网络错误，获取图片失败，请稍后再试~")
        except Exception as e:
            logger.error(f"[astrbot_plugin_hw] 未知错误: {e}")
            yield event.plain_result("获取图片失败，请稍后再试~")

    async def terminate(self):
        """插件卸载/停用时调用"""
        pass
