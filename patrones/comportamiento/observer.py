import weakref


class EventListener(object):
    def __init__(self):
        self.__REGISTERED_SIGNALS__ = {}

    def on(self, signal_name, callback):
        self.__REGISTERED_SIGNALS__[signal_name] = callback

    def respond(self, signal_name, *args, **kwargs):
        if signal_name in self.__REGISTERED_SIGNALS__:
            self.__REGISTERED_SIGNALS__[signal_name](*args, **kwargs)


class EventThrower(object):
    def __init__(self):
        self.__LISTENERS__ = []

    def emit(self, signal_name, *args, **kwargs):
        dead_listeners = []
        for listener in self.__LISTENERS__:
            if listener() is None:
                dead_listeners.append(listener)
                continue
            listener().respond(signal_name, *args, **kwargs)
        for dead in dead_listeners:
            self.__LISTENERS__.remove(dead)

    def add_listener(self, listener):
        self.__LISTENERS__.append(weakref.ref(listener))


if __name__ == '__main__':
    def callback():
        print 'fui llamado'

    observer = EventListener()
    observed = EventThrower()

    observed.add_listener(observer)

    observer.on('un_evento', callback)

    observed.emit('un_evento')
