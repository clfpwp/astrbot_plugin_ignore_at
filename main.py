from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import At

@register("ignore_at_all", "Your Name", "一个忽略包含@全体成员消息的插件", "1.0.0", "repo url")
class IgnoreAtAllPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.event_message_type(filter.EventMessageType.ALL)
    async def ignore_at_all(self, event: AstrMessageEvent):

        for comp in event.message_obj.message:
            if isinstance(comp, At):
                if str(comp.qq).lower() in {"all", "全体成员"}:
                    logger.info("检测到为@全体成员，停止事件传播。")
                    event.stop_event()
                    return
