from .handles import Attachable
from ..core.bus import Bus
from ..core.bits import Bridge


HIGHLIGHT_COLOR = "#F08"
PIN_COLOR = "#FB0"
class Wire(Attachable):
	def __init__(self):
		Attachable.__init__(self, Bus)
		self.path = []

	def get_back(self, *tags):
		if len(tags) == 1:
			connection = int(tags[0])
			return (self.device[connection], f"pin_{pin}")
		return tags

	def draw(self):
		d = 0.2
		self.delete()
		self.env.translate(0.5, 0.5)
		for i, (_, _, x, y) in enumerate(self.path):
			if i > 0:
				self._draw("line", ox, oy, x, y, fill=PIN_COLOR)
			self._draw("rect", x-d, y-d, x+d, y+d, name="caps", fill=PIN_COLOR)
			ox, oy = x, y
		self.apply(self.env.can.tag_raise, "caps")
		self.env.translate()

	def on_create(self, handle):
		self.path = handle.args
		self.draw()

	def on_destroy(self, handle):
		self.delete()

	def on_move(self, handle):
		self.draw()

	def on_key(self, code, handle):
		self.draw()

	def on_button(self, handle):
		num, press, x, y = handle.args[-1]
		if not press and num in (2, 3) and isinstance(self.env.select, Bridge):
			self.device.connect(self.env.select)
		if num == 3 and not press:
			handle.release()
		return num == 2 and not press

	def on_hand_over(self, button, press, x, y, cursor):
		if button==3 and not press:
			cursor.attach(self, apply_state=False)
		elif button==2 and not press:
			cursor.attach(Wire(), apply_state=False)
			cursor.handle.button(button, press, x, y)

	def on_update(self):
		fill = HIGHLIGHT_COLOR if self.device.value else PIN_COLOR
		self.apply(self.env.can.itemconfig, fill=fill)
