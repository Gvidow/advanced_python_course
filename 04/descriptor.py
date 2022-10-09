class BaseDescriptor:
    def __set_name__(self, owner, name):
        self.name = "__" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if self.check(value):
            setattr(instance, self.name, value)
        else:
            raise TypeError

    def __delete__(self, instance):
        delattr(instance, self.name)

    @classmethod
    def check(cls, val):
        return True


class Integer(BaseDescriptor):
    @classmethod
    def check(cls, val):
        return isinstance(val, int)


class String(BaseDescriptor):
    @classmethod
    def check(cls, val):
        return isinstance(val, str)


class PositiveInteger(BaseDescriptor):
    @classmethod
    def check(cls, val):
        return isinstance(val, int) and val > 0


class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price
