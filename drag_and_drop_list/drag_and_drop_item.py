from typing import Any, Optional

from flet import (
    Draggable,
    DragTarget,
    Container,
    colors,
    Column,
)

# from flet_core.control import Control
# from flet_core.ref import Ref
# from flet_core.event_handler import EventHandler
from .event import Event


class DragAndDropItem(Container):
    initial_bgcolor = None
    on_drop = Event()
    drop_place_holder = None

    def init(self):
        self.drop_place_holder = Container(width=self.content.width, height=20, bgcolor=colors.CYAN_900, visible=False)
        self.content = Draggable(
            content=DragTarget(
                content=Column(controls=[self.drop_place_holder, self.content], spacing=0),
                on_accept=self._on_accept,
                on_leave=self._on_leave,
                on_will_accept=self._on_will_accept,
            ),
        )
        self.initial_bgcolor = self.bgcolor
        return self

    def _on_accept(self, e):
        # source = self.page.get_control(e.src_id).content.content
        # target = self.content.content.content
        source = self.page.get_control(e.src_id)
        target = self.content

        self.on_drop(source, target)
        print('on_accept', e)
        self.bgcolor = self.initial_bgcolor
        self.drop_place_holder.visible = False
        self.page.update()

    def _on_will_accept(self, e):
        print('on_will_accept', e)
        self.bgcolor = colors.RED
        self.drop_place_holder.visible = True
        self.page.update()

    def _on_leave(self, e):
        print('on_leave', e)
        self.bgcolor = self.initial_bgcolor
        self.drop_place_holder.visible = False
        self.page.update()
