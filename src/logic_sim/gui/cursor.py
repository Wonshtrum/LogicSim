from .handles import Handle


class Cursor:
	def __init__(self, env):
		self.env = env
		self.x = 0
		self.y = 0
		self.handle = None
		self.auto_supply = True
		self.save_state = {"angle":0}

	def update(self, x, y):
		self.x = x
		self.y = y

	def attach(self, attachable, apply_state=True):
		attachable.env = self.env
		if self.handle is not None:
			self.handle.release(destroy=True)
		if apply_state:
			self.handle = Handle(attachable, self, self.save_state)
		else:
			self.handle = Handle(attachable, self)

	def hand_over(*_args, propagate=True, **_kwargs):
		def decorator(func):
			def wrapper(self, *args, **kwargs):
				if self.handle is not None:
					func(self, *_args, *args, **_kwargs, **kwargs)
				elif propagate and self.env.group_select is not None:
					self.env.group_select.on_hand_over(*_args, *args, self, **_kwargs, **kwargs)
			return wrapper
		return decorator

	@hand_over(propagate=False)
	def key(self, code):
		self.handle.key(code)

	@hand_over(propagate=False)
	def move(self, x, y):
		self.handle.move(x, y)

	@hand_over(1, True)
	def b1(self, button, press, x, y):
		self.handle.button(button, press, x, y)

	@hand_over(2, True)
	def b2(self, button, press, x, y):
		self.handle.button(button, press, x, y)

	@hand_over(3, True)
	def b3(self, button, press, x, y):
		self.handle.button(button, press, x, y)

	@hand_over(1, False)
	def b1r(self, button, press, x, y):
		self.handle.button(button, press, x, y)

	@hand_over(2, False)
	def b2r(self, button, press, x, y):
		self.handle.button(button, press, x, y)

	@hand_over(3, False)
	def b3r(self, button, press, x, y):
		self.handle.button(button, press, x, y)
