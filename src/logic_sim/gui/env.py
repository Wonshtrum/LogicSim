import tkinter as tk
from .cursor import Cursor
from math import cos, sin


def int_(x):
	return int(x//1)


class Env:
	actions = {
		"Motion": "move",
		"Button-1": "b1",
		"Button-2": "b2",
		"Button-3": "b3",
		"ButtonRelease-1": "b1r",
		"ButtonRelease-2": "b2r",
		"ButtonRelease-3": "b3r",
	}
	def __init__(self, win, col=30, row=30, scale=4, ox=0, oy=0, label=None, **kwargs):
		self.win = win
		self.cursor = Cursor(self)
		self.scale = 2**scale
		self.ox = ox
		self.oy = oy
		self.dx = 0
		self.dy = 0
		self.x = 0
		self.y = 0
		self.cos = None
		self.sin = None
		self.label = label
		self.draws = {}

		self.can = tk.Canvas(
			win,
			width=col*self.scale,
			height=row*self.scale,
			xscrollincrement=1,
			yscrollincrement=1,
			**kwargs)

		self.draw_commands = {
			"rect": self.can.create_rectangle,
			"line": self.can.create_line,
			"poly": self.can.create_polygon
		}

		for event, callback in Env.actions.items():
			self.bind(event, self.callback(callback))
		self.bind("Key", lambda event: self.cursor.key(event.keycode))

		self.bind("Button-1", self.scroll_start)
		self.bind("B1-Motion", self.scroll_move)
		self.bind("Button-4", self.zoom)
		self.bind("Button-5", self.zoom)
		self.bind("MouseWheel", self.zoom)

	def callback(self, name):
		callback = getattr(self.cursor, name)
		def bind(event):
			self.can.focus_set()
			x, y = self.position(event)
			self.cursor.update(x, y)
			callback(x, y)
		return bind

	def bind(self, event, callback):
		self.can.bind(f"<{event}>", callback, add="+")

	def add_handle(self, handle):
		tag = f"_{id(handle)}"
		self.draws[tag] = handle
		self.can.itemconfigure(tag, state="normal")

	def get_back(self):
		tags = self.can.gettags("current")
		self.select = self.group_select = None
		if len(tags) > 1:
			*tags, _id, _ = tags
			obj = self.draws.get(_id, None)
			self.group_select = obj
			if obj is not None:
				try:
					self.select = obj.get_back(*tags)
					return (obj, self.select)
				except Exception:
					pass
			return (*tags, _id)
		return tags
		
	def position(self, event):
		x, y = int_((event.x+self.ox-1)/self.scale), int_((event.y+self.oy-1)/self.scale)
		infos = self.get_back()
		if self.label is not None:
			self.label.set(f"({x} ; {y})\t{infos}")
		return x, y

	def rotate(self, angle=None, x=None, y=None):
		if x is not None: self.x = x
		if y is not None: self.y = y
		if angle is None:
			self.cos = None
			self.sin = None
			self.x = 0
			self.y = 0
		else:
			angle %= 4
			angle *= 3.14159265358979323/2
			self.cos = cos(angle)
			self.sin = sin(angle)

	def translate(self, dx=0, dy=0):
		self.dx = dx
		self.dy = dy

	def draw(self, shape, *args, **kwargs):
		if "width" not in kwargs:
			kwargs["width"] = 0
		c, s, x, y, dx, dy = self.cos, self.sin, self.x, self.y, self.dx, self.dy
		args = zip(args[::2], args[1::2])
		if self.cos is None:
			coords = [(a+dx, b+dy) for a,b in args]
		else:
			coords = [((a-x)*c+(b-y)*s+x+dx, -(a-x)*s+(b-y)*c+y+dy) for a,b in args]
		coords = [_*self.scale for xy in coords for _ in xy]
		return self.draw_commands[shape](coords, **kwargs)

	def zoom(self, event):
		direction = event.num == 4 or event.delta>0
		factor = 2 if direction else 1/2
		new_scale = min(max(self.scale*factor, 1), 128)
		if new_scale != self.scale:
			self.scale = new_scale
			dx = event.x+self.ox
			dy = event.y+self.oy
			self.can.scale("all", 0, 0, factor, factor)
			self.can.xview_scroll(int(dx*(factor-1)), "units")
			self.can.yview_scroll(int(dy*(factor-1)), "units")
			self.update_origin()

	def update_origin(self):
		self.ox = self.can.canvasx(0)
		self.oy = self.can.canvasy(0)

	def scroll_start(self, event):
		self.can.scan_mark(event.x, event.y)
	def scroll_move(self, event):
		self.can.scan_dragto(event.x, event.y, gain=1)
		self.update_origin()
