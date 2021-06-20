from logic_sim import *


def visit_all():
	for handle in env.draws.values():
		ctx.visit(handle.device)

def tick():
	ctx.update()
	env.update_handles(ctx.visited)


ctx = Context("Main ctx")

BG_COLOR = "#0d1117"
win = tk.Tk()
win.title("LogicSim")
win.configure(bg=BG_COLOR)
txt = tk.StringVar()
label = tk.Label(win, textvariable=txt)

env = Env(win, bg=BG_COLOR, highlightthickness=0, label=txt)
env.can.pack()
label.pack(side=tk.LEFT)

Menu = tk.Menu
menuBar = Menu(win)
menuFile = Menu(menuBar, tearoff=0)
def attach(device):
	env.cursor.attach(device(), apply_state=False)
	env.cursor.auto_supply = True

for device in (Chip_Not, Chip_And, Chip_Or, Chip_Xor, Chip_Nand, Chip_Nor, Chip_Device, Wire):
	menuFile.add_command(label=device.__name__, command=bind(attach, device))
menuBar.add_cascade(label="Devices", menu=menuFile)
win.config(menu = menuBar)

env.draw("rect", 0,0,1,1, fill="red", width=0)
a = Chip_Not()
env.cursor.attach(a)
#win.mainloop()
