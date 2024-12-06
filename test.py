import random

def func(a):
    a.pop()

x = set()

x.add(1)
x.add(2)
x.add(3)
x.add(4)

t = random.choice(list(x))
x.remove(t)

print(t,x)







