class EnumDict:
    def __iter__(self):
        for a in dir(type(self)):
            if not a.startswith("__"):
                yield a, getattr(self, a)
