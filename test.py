class A(object):
    def __dict__(self):
        return {}


class B(object):
    def __dict__(self):
        return {10: 10}


class C(B, A):
    pass


import datetime

print(datetime.datetime.today())

b = {1: 2, 3: 4}
for r in b:
    print(r)
