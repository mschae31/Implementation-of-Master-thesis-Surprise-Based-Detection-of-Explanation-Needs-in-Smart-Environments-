import numpy as np
from scipy.stats import dirichlet
from scipy.special import gamma
from scipy import special
import math
import time


a = np.ones(2, dtype="int64")
print(a)
print(type(a[0]))
a = np.append(a, 1)
print(a)
print(type(a[2]))
b = ["test"]
b.append("test2")
print(type(b[1]))


print("Second test")
#test change number 2

string = "test"

print(b)

c=b[0]

print(c)

c="changed"
print(c)
print(b)
b[0]=c
print(b)
