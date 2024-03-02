from typing import Any, List, Optional, Union

from flet import (
    ListView,
    Draggable,
    DragTarget,
    Container,
    colors,
)
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import (
    AnimationValue,
    OffsetValue,
    PaddingValue,
    ResponsiveNumber,
    RotateValue,
    ScaleValue,
)

from .drag_and_drop_item import DragAndDropItem


class DragAndDropListView(ListView):
    def __init__(
            self,
            controls: Optional[List[Control]] = None,
            ref: Optional[Ref] = None,
            key: Optional[str] = None,
            width: OptionalNumber = None,
            height: OptionalNumber = None,
            left: OptionalNumber = None,
            top: OptionalNumber = None,
            right: OptionalNumber = None,
            bottom: OptionalNumber = None,
            expand: Union[None, bool, int] = None,
            expand_loose: Optional[bool] = None,
            col: Optional[ResponsiveNumber] = None,
            opacity: OptionalNumber = None,
            rotate: RotateValue = None,
            scale: ScaleValue = None,
            offset: OffsetValue = None,
            aspect_ratio: OptionalNumber = None,
            animate_opacity: AnimationValue = None,
            animate_size: AnimationValue = None,
            animate_position: AnimationValue = None,
            animate_rotation: AnimationValue = None,
            animate_scale: AnimationValue = None,
            animate_offset: AnimationValue = None,
            on_animation_end=None,
            visible: Optional[bool] = None,
            disabled: Optional[bool] = None,
            data: Any = None,
            #
            # ScrollableControl specific
            #
            auto_scroll: Optional[bool] = None,
            reverse: Optional[bool] = None,
            on_scroll_interval: OptionalNumber = None,
            on_scroll: Any = None,
            #
            # Specific
            #
            horizontal: Optional[bool] = None,
            spacing: OptionalNumber = None,
            item_extent: OptionalNumber = None,
            first_item_prototype: Optional[bool] = None,
            divider_thickness: OptionalNumber = None,
            padding: PaddingValue = None,
            #
            # Adaptive
            #
            adaptive: Optional[bool] = None,
    ):
        controls_updated = []
        for i, c in enumerate(controls):
            c = DragAndDropItem(
                content=c,
                bgcolor=colors.TRANSPARENT,  # colors.AMBER_200 if i % 2 else colors.GREEN_200,
                height=getattr(c, 'width', None),
                width=getattr(c, 'height', None),
            ).init()
            c.on_drop.add(self._on_drop_item)
            controls_updated.append(c)
        super(DragAndDropListView, self).__init__(
            controls_updated,
            ref,
            key,
            width,
            height,
            left,
            top,
            right,
            bottom,
            expand,
            expand_loose,
            col,
            opacity,
            rotate,
            scale,
            offset,
            aspect_ratio,
            animate_opacity,
            animate_size,
            animate_position,
            animate_rotation,
            animate_scale,
            animate_offset,
            on_animation_end,
            visible,
            disabled,
            data,
            auto_scroll,
            reverse,
            on_scroll_interval,
            on_scroll,
            horizontal,
            spacing,
            item_extent,
            first_item_prototype,
            divider_thickness,
            padding,
            adaptive,
        )

    def _on_drop_item(self, source, target):
        print(f"{self.__class__.__name__}._on_drop_item({source=}, {target=})")

        source = self.__get_item(source)
        target = self.__get_item(target)
        if source is target or source is None or target is None:
            return

        self.controls.remove(source)
        insert_index = self.controls.index(target)

        self.controls.insert(insert_index, source)
        self.page.update()

    def __get_item(self, ritem) -> Optional[DragAndDropItem]:
        for litem in self.controls:
            if litem.content is ritem:
                return litem
