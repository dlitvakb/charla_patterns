class AbstractFactory(object):
    def __new__(cls, class_name=None, *args, **kwargs):
        if class_name is not None:
            return globals()[class_name](*args, **kwargs)
        return object.__new__(cls, *args, **kwargs)

    def __init__(self, class_name=None, *args, **kwargs):
        pass

class A(object):
    pass

class B(object):
    pass


if __name__ == '__main__':
    print AbstractFactory('A').__class__.__name__
    print AbstractFactory('B').__class__.__name__

    print AbstractFactory('AbstractFactory').__class__.__name__
    print AbstractFactory().__class__.__name__
