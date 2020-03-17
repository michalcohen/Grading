import json


class A:
    def __init__(self, x=None, a=None):
        if x:
            self.x = x
            self.y = 0
        else:
            self.x = a.x
            self.y = a.y

    def __deepcopy__(self, memodict={}):
        return A(a=self)


class DictToObject(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [DictToObject(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, DictToObject(b) if isinstance(b, dict) else b)


class B:
    def __init__(self, x=None, b=None):
        if x:
            self.a = A(x)
            self.z = -1
        else:
            self.a = A(a=b.a)
            self.z = b.z

    def __deepcopy__(self, memodict={}):
        return B(b=self)

    def save(self, file_name):
        with open(file_name, "w") as f:
            return json.dump(self, f, default=lambda o: getattr(o, '__dict__', str(o)), indent="\t")

    @classmethod
    def load(cls, file_name):
        with open(file_name, "r") as f:
            d = DictToObject(json.load(f))
            p = B(b=d)
            return p


# b = B(5)
# b.save("banana.json")
b = B.load("banana.json")
print(b.a.y)
