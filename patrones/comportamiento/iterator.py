class IteratorSimple(object):
    def __init__(self, _list):
        self._list = _list

    def __iter__(self):
        return self._list.__iter__()


class ListIterator(list):
    pass

if __name__ == '__main__':
    it = IteratorSimple([1, 2, 3, 4])
    for x in it:
        print x

    try:
        it.append(4)
    except AttributeError:
        print "Esto falla"

    print '\n\n\n'

    lit = ListIterator([1, 2, 3, 4])
    for x in lit:
        print x

    lit.append(10)
    print lit[4]
