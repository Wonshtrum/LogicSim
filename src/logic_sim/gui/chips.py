from .handles import Drawable, Attachable
from ..utils import super_init
from ..devices import *
from math import pi


CHIP_COLOR = "#447"
HIGHLIGHT_COLOR = "#F08"
PIN_COLOR = "#FB0"
class Chip(Drawable, Attachable):
	def __init__(self, device, width, height, pins=None, map_pins=None, env=None):
		Drawable.__init__(self, env)
		Attachable.__init__(self, device)
		self.width = width
		self.height = height
		self.angle = 0

		if pins is None:
			pins = [1]*width*2
		if map_pins is None:
			map_pins = [pin*sum(pins[:i+1])-1 for i,pin in enumerate(pins)]

		self.pins = pins
		self.map_pins = map_pins
	
	def draw(self):
		x, y, w, h = self.x, self.y, self.width, self.height
		d = 0.2
		self.delete()
		if w%2 or h%2:
			self.env.rotate(self.angle, (w-1)//2+0.5, (h-1)//2+0.5)
			self.env.translate(x-(w-1)//2, y-(h-1)//2)
		else:
			self.env.rotate(self.angle, w//2, h//2)
			self.env.translate(x-w//2, y-h//2)
		self._draw("rect", 0, 0, w, h, fill=CHIP_COLOR)
		self._draw("rect", d, d, d*2.5, d*2.5, fill=HIGHLIGHT_COLOR)
		for i in range(w):
			if self.pins[i]:
				self._draw("rect", i+d, 0, i+1-d, -1+d*2, fill=PIN_COLOR)
		for i in range(w):
			if self.pins[i+w]:
				self._draw("rect", i+d, h, i+1-d, h+1-d*2, fill=PIN_COLOR)
		self.env.rotate()
		self.env.translate()

	def on_move(self, handle):
		_, _, x, y = handle.args[-1]
		self.move(x, y)

	def on_button(self, handle):
		num, press, x, y = handle.args[-1]
		if num != 3 or press:
			return False
		handle.release()

	def on_key(self, code, handle):
		if code == 65:
			self.angle = (self.angle+1)%4
			self.draw()


@super_init(Not, 1, 1)
class Chip_Not(Chip):
	pass

@super_init(And, 3, 2, [1,0,1,0,1,0])
class Chip_And(Chip):
	pass

@super_init(Or, 3, 2, [1,0,1,0,1,0])
class Chip_Or(Chip):
	pass

@super_init(Xor, 3, 2, [1,0,1,0,1,0])
class Chip_Or(Chip):
	pass

@super_init(Nand, 3, 2, [1,0,1,0,1,0])
class Chip_Nand(Chip):
	pass

@super_init(Nor, 3, 2, [1,0,1,0,1,0])
class Chip_Nor(Chip):
	pass

@super_init(Device, 8, 4)
class Chip_Device(Chip):
	pass
