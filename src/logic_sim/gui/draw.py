class Drawable:
	default = {
		"activefill": "white",
		"disabledstipple": "gray50",
		"state": "disabled",
	}
	def __init__(self, env=None):
		self.env = env
		self.shapes = {}
		self.x = 0
		self.y = 0
		self.angle = 0

	def get_back(self, *tags):
		return tags
	
	def get_id(self):
		return "_{id(self)}"

	def _draw(self, *args, name="_", **kwargs):
		if not name in self.shapes:
			self.shapes[name] = []
		tags = kwargs.get("tags", [])
		tags.append(self.get_id())
		kwargs["tags"] = tags

		for key, value in self.default.items():
			kwargs[key] = kwargs.get(key, value)

		self.shapes[name].append(self.env.draw(*args, **kwargs))

	def apply(self, func, *names, **kwargs):
		if not names:
			names = self.shapes
		for name in names:
			for shape in self.shapes[name]: func(shape, **kwargs)

	def move(self, x, y):
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
