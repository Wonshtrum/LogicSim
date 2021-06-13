from .handles import Handle


class Cursor:
	def __init__(self, env):
		self.env = env
		self.x = None
		self.y = None
		self.handle = None

	def update(self, x, y):
		self.x = x
		self.y = y

	def attach(self, attachable):
		attachable.env = self.env
		self.handle = Handle(attachable, self)

	def hand_over(func):
		def wrapper(self, *args, **kwargs):
			if self.handle is not None:
				func(self, *args, **kwargs)
		return wrapper

	@hand_over
	def key(self, code):
		self.handle.key(code)

	@hand_over
	def move(self, x, y):
		self.handle.move(x, y)

	@hand_over
	def b1(self, x, y):
		self.handle.button(1, True, x, y)

	@hand_over
	def b2(self, x, y):
		self.handle.button(2, True, x, y)

	@hand_over
	def b3(self, x, y):
		#self.env.draw("rect", x,y,x+1,y+1, fill="red", width=0)
		self.handle.button(3, True, x, y)

	@hand_over
	def b1r(self, x, y):
		self.handle.button(1, False, x, y)

	@hand_over
	def b2r(self, x, y):
		self.handle.button(2, False, x, y)

	@hand_over
	def b3r(self, x, y):
		self.handle.button(3, False, x, y)