from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At

@register("ignore_at_all", "Cl_Fu", "一个忽略包含@全体成员,以及关闭@机器人回复的插件，可通过指令开关@功能", "1.0.0")
class IgnoreAtAllPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.ignore_all_at = False

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def ignore_at_all(self, event: AstrMessageEvent):

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
        self.ignore_all_at = True
        yield event.plain_result("无视@功能已开启。")

    @filter.permission_type(filter.PermissionType.ADMIN)
    @filter.command("ignore_at_off")
    async def ignore_at_off(self, event: AstrMessageEvent):

        self.ignore_all_at = False
        yield event.plain_result("无视@功能已关闭。")
