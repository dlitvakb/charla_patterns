class LoggingProxy(object):
    def __init__(self, obj):
        self.real_object = obj

    def __getattr__(self, name, *args, **kwargs):
        attr = getattr(self.real_object, name, None)
        if attr is not None:
            print("Before executing {0}".format(name))
            return attr
        else:
            raise AttributeError(
                '{0} has no attribute {1}'.format(
                    self.real_object.__class__.__name__,
                    name
                )
            )

class Saludador(object):
    def hola(self):
        return "hola mundo"

if __name__ == '__main__':
    saludador = LoggingProxy(Saludador())
    print(saludador.hola())

    print('\n\n\n')

    print(saludador.lalalala()) # Quiero que este falle
