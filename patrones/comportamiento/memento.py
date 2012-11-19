class Saludador(object):
    def __init__(self, nombre):
        self.nombre = nombre

    def hola(self):
        print "hola %s" % self.nombre

    def guardar_estado(self):
        estado = {}
        estado.update(self.__dict__)
        return estado

    def recuperar_estado(self, estado):
        self.__dict__.update(estado)

if __name__ == '__main__':
    s = Saludador('David')
    estados = []

    s.hola()
    estados.append(s.guardar_estado())

    s.nombre = 'Florencia'
    s.hola()
    estados.append(s.guardar_estado())

    s.nombre = 'Emiliano'
    s.hola()
    estados.append(s.guardar_estado())

    for estado in estados:
        s.recuperar_estado(estado)
        s.hola()

