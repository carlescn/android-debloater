import logging
from enum import Enum

log = logging.getLogger(__name__)

events: dict[Enum, set[callable]] = {}


def register(event: Enum, handler: callable):
    if event in events:
        events.get(event).add(handler)
    else:
        events[event] = {handler}
    log.debug("Registered handler '%s' for event '%s'", handler.__qualname__, event.name)


def unregister(event: Enum, handler: callable):
    if event not in events:
        log.error("Unable to unregister handler '%s' for event '%s': event not registered",
                  handler.__qualname__, event.name)
        return

    if handler not in events.get(event):
        log.error("Unable to unregister handler '%s' for event '%s': handler not registered",
                  handler.__qualname__, event.name)
        return

    handlers = events.get(event)
    handlers.remove(handler)
    log.debug("Unregistered handler '%s' for event '%s'", handler.__qualname__, event.name)

    if handlers == set():
        events.pop(event)
        log.debug("Unregistered empty event '%s'", event.name)


def fire(event: Enum, *args, **kwargs):
    if event not in events:
        log.error("Unable to fire event '%s': event not registered", event.name)
        return

    if events.get(event) == set():
        log.debug("Fired event '%s', but it has no handlers", event.name)
        return

    log.debug("Firing event '%s'", event.name)
    for handler in events.get(event):
        handler(*args, **kwargs)
