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

if ("test22" in b):
    print("ja")
else:
    print("ne")

b.append("test")
b[0] = "test0"
print(b.index("test"))