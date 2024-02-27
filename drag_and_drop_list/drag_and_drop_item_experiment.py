from typing import Callable
from enum import StrEnum, auto

from flet import (
    Draggable,
    DragTarget,
    Container,
    colors,
    Column,
    Stack,
    Page,
)

from .event import Event


class DropLocation(StrEnum):
    BEFORE = auto()
    AFTER = auto()


def _create_placeholder(widht: int) -> Container:
    return Container(
        width=widht,
        height=20,
        bgcolor=colors.CYAN_900,
        # bgcolor=colors.TRANSPARENT,
        visible=False,
    )


def fabric(component: Container, page: Page) -> dict[str, Callable]:
    def on_accept(_):
        component.visible = False
        page.update(component)

    def on_leave(_):
        component.visible = False
        page.update(component)

    def on_will_accept(_):
        component.visible = True
        page.update(component)

    methods = {
        'on_accept': on_accept,
        'on_leave': on_leave,
        'on_will_accept': on_will_accept,
    }
    return methods


class DragAndDropItem(Container):
    initial_bgcolor = None
    on_drop = Event()
    drop_place_holder_top = None
    drop_place_holder_bot = None
    trigger_top = None
    trigger_bot = None

    def init(self):
        width = getattr(self.content, 'width', None)
        height = 20
        self.drop_place_holder_top = _create_placeholder(width)
        self.drop_place_holder_bot = _create_placeholder(width)
        self.trigger_top = DragTarget(content=Container(width=width, height=height // 2 if height else height, bgcolor=colors.TRANSPARENT),
                                      on_accept=self._on_accept_fabric(self.drop_place_holder_top),
                                      on_will_accept=self._on_will_accept_fabric(self.drop_place_holder_top),
                                      on_leave=self._on_leave_fabric(self.drop_place_holder_top),
                                      )
        self.trigger_bot = DragTarget(content=Container(width=width, height=height // 2 if height else height, bgcolor=colors.TRANSPARENT),
                                      on_accept=self._on_accept_fabric(self.drop_place_holder_bot),
                                      on_will_accept=self._on_will_accept_fabric(self.drop_place_holder_bot),
                                      on_leave=self._on_leave_fabric(self.drop_place_holder_bot),
                                      )

        self.content = Draggable(
            content=DragTarget(
                content=Column(controls=[
                    self.drop_place_holder_top,
                    Stack(controls=[self.content, Column(controls=[self.trigger_top, self.trigger_bot], spacing=0)]),
                    self.drop_place_holder_bot,
                ], spacing=0),
                on_accept=self._on_accept,
            ),
        )
        self.initial_bgcolor = self.bgcolor
        return self

    def _on_accept_fabric(self, placeholder: Container):
        def _on_accept(_):
            placeholder.visible = False
            self.page.update()
        return _on_accept

    def _on_accept(self, e):
        source = self.page.get_control(e.src_id)
        target = self.content

        self.on_drop(source, target)
        print('on_accept', e)
        self.bgcolor = self.initial_bgcolor
        self.drop_place_holder_top.visible = False
        self.drop_place_holder_bot.visible = False
        self.page.update()

    def _on_will_accept_fabric(self, placeholder: Container):
        def _on_will_accept(e):
            print('on_will_accept', e)
            self.bgcolor = colors.RED
            placeholder.visible = True
            self.page.update()
        return _on_will_accept

    def _on_leave_fabric(self, placeholder: Container):
        def _on_leave(e):
            print('on_leave', e)
            self.bgcolor = self.initial_bgcolor
            placeholder.visible = False
            self.page.update()
        return _on_leave
