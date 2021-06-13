from .draw import Drawable


class Handle:
	def __init__(self, host, cursor):
		self.host = host
		self.cursor = cursor
		self.args = [[None, None, None, None]]

	def button(self, num, press, x, y):
		head = self.args.pop()
		self.args.append([num, press, x, y])
		if self.host.on_button(self) is False:
			self.args.pop()
		self.args.append(head)

	def key(self, code):
		if code == 9 and len(self.args)>1:
			self.args.pop()
		self.host.on_key(code, self)

	def move(self, x, y):
		if (x, y) != self.args[-1][2:]:
			self.args[-1][2] = x
			self.args[-1][3] = y
			self.host.on_move(self)
	
	def release(self):
		self.cursor.handle = None


class Attachable:
	def __init__(self, device):
		self.device = device()

	def on_key(self, code, handle):
		print(code)
		pass
	def on_move(self, handle):
		print(handle.args)
		pass
	def on_button(self, handle):
		print(handle.args)
		num, press, _, _ = handle.args[-1]
		return num == 3 and not press
	
	def __repr__(self):
		return f"[{self.device}]"


class Chip(Drawable, Attachable):
	def __init__(self, device, width, height, pins=None, map_pins=None, env=None):
		Drawable.__init__(self, env)
		Attachable.__init__(self, device)
		self.width = width
		self.height = height

		if pins is None:
			pins = list(range(width*2))
		if map_pins is None:
			map_pins = [pin*sum(pins[:i+1])-1 for i,pin in enumerate(pins)]

		self.pins = pins
		self.map_pins = map_pins
	
	def draw(self):
		x, y, w, h = self.x, self.y, self.width, self.height
		self.delete()
		self._draw("rect", x, y, x+w, y+h, fill="#223")
		d = 0.2
		for i in range(w):
			if self.pins[i]:
				self._draw("rect", i+x+d, y,   i+x+1-d, y-1+d*2,   fill="#DB0")
		for i in range(w):
			if self.pins[i+w]:
				self._draw("rect", i+x+d, y+h, i+x+1-d, y+h+1-d*2, fill="#DB0")

	def on_move(self, handle):
		_, _, x, y = handle.args[-1]
		self.move(x, y)

	def on_button(self, handle):
		num, press, x, y = handle.args[-1]
		if num != 3 or press:
			return False
		handle.release()
