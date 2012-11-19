class Persona(object):
    def __init__(self):
        self._estado = EstadoBebe()

    def __getattribute__(self, name, *args, **kwargs):
        if name == 'crece':
            self._estado = EstadoGrande()
            return lambda: None
        if name != '_estado':
            attr = getattr(self._estado, name, None)
            if attr is not None:
                return attr
            else:
                print 'No puedo soy muy %s' % self._estado.calificativo
                return lambda: None
        else:
            return object.__getattribute__(self, '_estado')

class EstadoBebe(object):
    calificativo = 'chiquitoooo'

    def gatear(self):
        print 'gateoooo'

class EstadoGrande(object):
    calificativo = 'grandoteee'

    def caminar(self):
        print 'caminoooo'


if __name__ == '__main__':
    p = Persona()

    p.gatear()
    p.caminar()

    p.crece()

    p.gatear()
    p.caminar()
