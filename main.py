from logic_sim import *


ctx = Context("Main ctx")

bus = Bus()
n0, n1, n2 = [Not()  for _ in range(3)]
a0, a1, a2 = [And()  for _ in range(3)]
b0, b1, b2 = [Nand() for _ in range(3)]
c0, c1, c2 = [Nor()  for _ in range(3)]


BG_COLOR = "#0d1117"
win = tk.Tk()
win.title("LogicSim")
win.configure(bg=BG_COLOR)
txt = tk.StringVar()
label = tk.Label(win, textvariable=txt)

env = Env(win, bg=BG_COLOR, highlightthickness=0, label=txt)
env.can.pack()
label.pack(side=tk.LEFT)

env.draw("rect", 0,0,1,1, fill="red", width=0)
a = Chip_Nand()
env.cursor.attach(a)
#win.mainloop()
