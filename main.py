import os
import json
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At

@register("astrbot_plugin_ignore_at", "Cl_Fu", "一个可切换无视@机器人和@全体成员的插件", "1.1.0")
class IgnoreAtPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.ignore_bot_at = False
        self.ignore_all_at = False

        self.config_file = os.path.join(os.path.dirname(__file__), "ignore_at_config.json")
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.ignore_bot_at = config.get("ignore_bot_at", False)
                    self.ignore_all_at = config.get("ignore_all_at", False)
                    logger.info(
                        f"加载上次的设置：无视@机器人{'开启' if self.ignore_bot_at else '关闭'}，无视@全体成员{'开启' if self.ignore_all_at else '关闭'}"
                    )
            except (json.JSONDecodeError, IOError) as e:
                logger.error(f"读取配置文件时发生错误: {e}")

    def save_config(self):
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "ignore_bot_at": self.ignore_bot_at,
                        "ignore_all_at": self.ignore_all_at,
                    },
                    f,
                    ensure_ascii=False,
                    indent=4,
                )
                logger.info(
                    f"保存当前设置：无视@机器人{'开启' if self.ignore_bot_at else '关闭'}，无视@全体成员{'开启' if self.ignore_all_at else '关闭'}"
                )
        except IOError as e:
            logger.error(f"保存配置文件时发生错误: {e}")

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def ignore_at(self, event: AstrMessageEvent):
        try:
            bot_qq = str(event.get_self_id())
        except Exception as e:
            logger.error(f"无法获取机器人QQ号: {e}")
            return

        for comp in event.message_obj.message:
            if isinstance(comp, At):
                if self.ignore_bot_at and str(comp.qq) == bot_qq:
                    event.stop_event()
                    return
                if self.ignore_all_at and str(comp.qq).lower() in {"all", "全体成员"}:
                    event.stop_event()
                    return

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("ignore_at_bot_on")
    async def ignore_at_bot_on(self, event: AstrMessageEvent):
        self.ignore_bot_at = True
        self.save_config()
        yield event.plain_result("无视@机器人功能已开启。")

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("ignore_at_bot_off")
    async def ignore_at_bot_off(self, event: AstrMessageEvent):
        self.ignore_bot_at = False
        self.save_config()
        yield event.plain_result("无视@机器人功能已关闭。")

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("ignore_at_all_on")
    async def ignore_at_all_on(self, event: AstrMessageEvent):
        self.ignore_all_at = True
        self.save_config()
        yield event.plain_result("无视@全体成员功能已开启。")

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("ignore_at_all_off")
    async def ignore_at_all_off(self, event: AstrMessageEvent):
        self.ignore_all_at = False
        self.save_config()
        yield event.plain_result("无视@全体成员功能已关闭。")
