from context import *
from devices import *
from bus import *
from gui import *
from utils import *


ctx = Context("Main ctx")

bus = Bus()
n0, n1, n2 = [Not()  for _ in range(3)]
a0, a1, a2 = [And()  for _ in range(3)]
b0, b1, b2 = [Nand() for _ in range(3)]
c0, c1, c2 = [Nor()  for _ in range(3)]


win = tk.Tk()
win.title("LogicSim")
txt = tk.StringVar()
label = tk.Label(win, textvariable=txt)

env = Env(win, label=txt)
env.can.pack()
label.pack(side=tk.LEFT)

env.draw("rect", 0,0,1,1, fill="black", width=0)
win.mainloop()
