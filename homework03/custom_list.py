class CustomList(list):
    def __isub__(self, other):
        self.extend([0] * (len(other) - len(self)))
        for i in range(min(len(self), len(other))):
            self[i] -= other[i]
        return self

    def __sub__(self, other):
        new_custom_list = self.custom_list(self.copy())
        new_custom_list -= other
        return new_custom_list

    def __rsub__(self, other):
        return self - other

    def __iadd__(self, other):
        self.extend([0] * (len(other) - len(self)))
        for i in range(min(len(self), len(other))):
            self[i] += other[i]
        return self

    def __add__(self, other):
        new_custom_list = self.custom_list(self.copy())
        new_custom_list += other
        return new_custom_list

    def __radd__(self, other):
        return self + other

    @staticmethod
    def custom_list(lst):
        return __class__(lst)
