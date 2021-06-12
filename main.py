from context import *
from devices import *
from bus import *
from utils import *


ctx = Context("Main ctx")

bus = Bus()
n0, n1, n2 = [Not()  for _ in range(3)]
a0, a1, a2 = [And()  for _ in range(3)]
b0, b1, b2 = [Nand() for _ in range(3)]
c0, c1, c2 = [Nor()  for _ in range(3)]
