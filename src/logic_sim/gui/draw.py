class Drawable:
	def __init__(self, env):
		self.env = env
		self.shapes = {}
		self.x = 0
		self.y = 0
	
	def _draw(self, *args, name="_", **kwargs):
		if not name in self.shapes:
			self.shapes[name] = []
		self.shapes[name].append(self.env.draw(*args, **kwargs))

	def move(self, x, y):
		if self.x != x or self.y != y:
			self.x = x
			self.y = y
			self.draw()
	
	def draw(self):
		pass

	def delete(self, *names):
		if not names:
			names = self.shapes
		for name in names:
			for shape in self.shapes[name]:
				self.env.can.delete(shape)
			self.shapes[name] = []
