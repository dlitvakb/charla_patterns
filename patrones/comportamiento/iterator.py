class IteratorSimple(object):
    def __init__(self, _list):
        self._list = _list

    def __iter__(self):
        return self._list.__iter__()

    def __getitem__(self, index):
        return self._list[index]


class ListIterator(list):
    def menores_a(self, numero):
        return [x for x in self if x < numero]

if __name__ == '__main__':
    print('Iterator con Implementors')
    it = IteratorSimple([1, 2, 3, 4])
    for x in it:
        print(x)

    print(it[1])

    try:
        it.append(4)
    except AttributeError:
        print("Esto falla")

    print('\n\n\n')

    print('Iterator extendiendo list')
    lit = ListIterator([1, 2, 3, 4])
    for x in lit:
        print(x)

    lit.append(10)
    print(lit[4])

    print(lit.menores_a(2))
