import os
import json
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At

@register("astrbot_plugin_ignore_at", "Cl_Fu", "一个忽略包含@全体成员,以及关闭@唤醒机器人的插件，可通过指令开关@功能", "1.0.1")
class IgnoreAtAllPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.ignore_all_at = False

        self.config_file = os.path.join(os.path.dirname(__file__), "ignore_at_config.json")
        self.load_config()

    def load_config(self):
        """加载上次的配置（如果有）"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.ignore_all_at = config.get("ignore_all_at", False)
                    logger.info(f"加载上次的设置：无视@功能 {'开启' if self.ignore_all_at else '关闭'}")
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"读取配置文件时发生错误: {e}")

    def save_config(self):
        """保存当前配置"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump({"ignore_all_at": self.ignore_all_at}, f, ensure_ascii=False, indent=4)
                logger.info(f"保存当前设置：无视@功能 {'开启' if self.ignore_all_at else '关闭'}")
        except IOError as e:
            logger.error(f"保存配置文件时发生错误: {e}")

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def ignore_at_all(self, event: AstrMessageEvent):
        """监听消息，判断是否包含@全体成员或者@机器人"""
        for comp in event.message_obj.message:
            if isinstance(comp, At):
                if self.ignore_all_at:
                    logger.info("检测到@消息且无视@功能开启。")
                    event.stop_event()
                    return
                if str(comp.qq).lower() in {"all", "全体成员"}:
                    logger.info("检测到@全体成员消息。")
                    event.stop_event()
                    return

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("ignore_at_on")
    async def ignore_at_on(self, event: AstrMessageEvent):
        """开启无视@功能"""
        self.ignore_all_at = True
        self.save_config()  # 保存配置
        yield event.plain_result("无视@功能已开启。")

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("ignore_at_off")
    async def ignore_at_off(self, event: AstrMessageEvent):
        """关闭无视@功能"""
        self.ignore_all_at = False
        self.save_config()  # 保存配置
        yield event.plain_result("无视@功能已关闭。")

