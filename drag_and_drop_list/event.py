from logging import getLogger
from typing import Callable, Any


logger = getLogger(__name__)
EventHandler = Callable[[Any], None]


class Event:
    def __init__(self):
        self._handlers: list[EventHandler] = []

    def __call__(self, *args) -> None:
        for handler in self._handlers:
            try:
                handler(*args)
            except Exception as e:
                logger.error(
                    f"ERROR: {self.__class__.__name__}.__call__({args}): {e.__class__.__name__}: {e}"
                )

    def add(self, handler: EventHandler) -> None:
        if handler not in self._handlers:
            self._handlers.append(handler)

    def remove(self, handler: EventHandler) -> None:
        if handler in self._handlers:
            self._handlers.remove(handler)
