from typing import Any, Optional

from flet import (
    Draggable,
    DragTarget,
    Container,
    colors,
)

# from flet_core.control import Control
# from flet_core.ref import Ref
# from flet_core.event_handler import EventHandler
from .event import Event


class DragAndDropItem(Container):
    initial_bgcolor = None
    on_drop = Event()

    def init(self):
        self.content = Draggable(
            content=DragTarget(
                content=self.content,
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
        self.page.update()

    def _on_will_accept(self, e):
        print('on_will_accept', e)
        self.bgcolor = colors.RED
        self.page.update()

    def _on_leave(self, e):
        print('on_leave', e)
        self.bgcolor = self.initial_bgcolor
        self.page.update()


# class DragAndDropItem(Draggable, DragTarget):
#     def __init__(
#             self,
#             ref: Optional[Ref] = None,
#             disabled: Optional[bool] = None,
#             visible: Optional[bool] = None,
#             data: Any = None,
#             #
#             # Specific
#             #
#             group: Optional[str] = None,
#             content: Optional[Control] = None,
#             #
#             # Draggable
#             #
#             content_when_dragging: Optional[Control] = None,
#             content_feedback: Optional[Control] = None,
#             #
#             # DragTarget
#             #
#             on_will_accept=None,
#             on_accept=None,
#             on_leave=None,
#     ):
#         super().__init__(
#             ref=ref,
#             disabled=disabled,
#             visible=visible,
#             data=data,
#         )
#
#         self.__on_accept: Optional[EventHandler] = None
#         self.__content: Optional[Control] = None
#
#         DragTarget.__init__(
#             self,
#             disabled,
#             visible,
#             data,
#             group,
#             content,
#             on_will_accept,
#             on_accept,
#             on_leave,
#         )
#
#         self.__content: Optional[Control] = None
#         self.__content_when_dragging: Optional[Control] = None
#         self.__content_feedback: Optional[Control] = None
#
#         Draggable.__init__(
#             self,
#             ref,
#             disabled,
#             visible,
#             data,
#             group,
#             content,
#             content_when_dragging,
#             content_feedback,
#         )
#
#     def _on_accept(self, e):
#         pass
#
#     def _on_will_accept(self, e):
#         pass
#
#     def _on_leave(self, e):
#         pass
