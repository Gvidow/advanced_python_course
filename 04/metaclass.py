class CustomMeta(type):
    class Custom:
        def __setattr__(self, name, val):
            super().__setattr__("custom_" + name, val)

    def __new__(mcs, name, bases, attrs, **kwargs):
        keys = list(attrs.keys())
        new_attrs = {}
        for key in keys:
            if len(key) > 4 and key[:2] + key[-2:] == "____":
                new_attrs[key] = attrs[key]
            else:
                new_attrs["custom_" + key] = attrs[key]
        return super().__new__(mcs, name, bases + (mcs.Custom,), new_attrs)

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs, **kwargs)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class CustomClass(metaclass=CustomMeta):
    x = 5

    def __init__(self, val):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
