import json


class DictToObject(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [DictToObject(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, DictToObject(b) if isinstance(b, dict) else b)


class Common:
    def save(self, file_name):
        with open(file_name, "w") as f:
            return json.dump(self, f, default=lambda o: getattr(o, '__dict__', str(o)), indent="\t")

    @classmethod
    def load(cls, file_name):
        with open(file_name, "r") as f:
            return cls(copy_from=DictToObject(json.load(f)))


class A(Common):
    def __init__(self, x=None, copy_from=None):
        if x:
            self.x = x
            self.y = 0
        else:
            self.x = copy_from.x
            self.y = copy_from.y

    def __deepcopy__(self, memodict={}):
        return A(copy_from=self)


class B(Common):
    def __init__(self, x=None, copy_from=None):
        if x:
            self.a = A(x)
            self.z = -1
        else:
            self.a = A(copy_from=copy_from.a)
            self.z = copy_from.z

    def logic(self, c):
        return (c + self.z) * (self.a.x - self.a.y)

    def __deepcopy__(self, memodict={}):
        return B(copy_from=self)



# a = A(8)
# a.save("a.json")
# b = B(5)
# b.save("b.json")
b = B.load("b.json")
print(b.a.y)
