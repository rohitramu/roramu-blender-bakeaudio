def property_getter(property_name: str):
    def getter(self):
        return self[property_name]

    return getter


def property_setter_fake():
    def __fake_setter(self, value):
        pass

    return __fake_setter


def property_setter(obj, property_name: str):
    def setter(value):
        obj[property_name] = value

    return setter
