from flet import (
    Draggable,
    DragTarget,
    Container,
    colors,
    Column,
)

from .event import Event


class DragAndDropItem(Container):
    initial_bgcolor = None
    on_drop = Event()
    drop_place_holder = None

    def init(self):
        width = getattr(self.content, 'width', None)
        self.drop_place_holder = Container(width=width, height=20, bgcolor=colors.CYAN_900, visible=False)
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
        source = self.page.get_control(e.src_id)
        target = self.content

        self.on_drop(source, target)
        print('on_accept', e)
        self.bgcolor = self.initial_bgcolor
        self.drop_place_holder.visible = False
        if self.page:
            self.page.update(self, self.drop_place_holder)

    def _on_will_accept(self, e):
        print('on_will_accept', e)
        self.bgcolor = colors.RED
        self.drop_place_holder.visible = True
        if self.page:
            self.page.update(self, self.drop_place_holder)

    def _on_leave(self, e):
        print('on_leave', e)
        self.bgcolor = self.initial_bgcolor
        self.drop_place_holder.visible = False
        if self.page:
            self.page.update(self, self.drop_place_holder)
