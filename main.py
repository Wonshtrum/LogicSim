from context import *
from devices import *


ctx = Context("base")

b0, b1, b2 = [Bus() for _ in range(3)]
n0, n1, n2 = [Not() for _ in range(3)]
a0 = And()
