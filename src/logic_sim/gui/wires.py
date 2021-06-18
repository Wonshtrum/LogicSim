from .handles import Attachable
from .draw import Drawable
from ..core.bus import Bus


HIGHLIGHT_COLOR = "#F08"
PIN_COLOR = "#FB0"
class Wire(Drawable, Attachable):
	def __init__(self, env=None):
		Drawable.__init__(self, env)
		Attachable.__init__(self, Bus)
		self.path = []

	def get_back(self, *tags):
		if len(tags) == 1:
			connection = int(tags[0])
			return (f"pin_{pin}", self.device[connection])
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
		if num == 3 and not press:
			handle.release()
		return num == 2 and not press	
