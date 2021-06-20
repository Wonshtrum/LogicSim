from .draw import Drawable


class Handle:
	def __init__(self, host, cursor, save_state=None):
		self.host = host
		self.cursor = cursor
		self.args = [[None, None, cursor.x, cursor.y]]
		if save_state is not None:
			for key, value in save_state.items():
				if hasattr(host, key):
					setattr(host, key, value)
		host.on_create(self)

	def button(self, num, press, x, y):
		head = self.args.pop()
		self.args.append([num, press, x, y])
		if self.host.on_button(self) is False:
			self.args.pop()
		self.args.append(head)

	def key(self, code):
		if code == 9:
			if len(self.args) > 1:
				self.args.pop(-2)
			else:
				self.release(destroy=True)
				return
		self.host.on_key(code, self)

	def move(self, x, y):
		if [x, y] != self.args[-1][2:]:
			self.args[-1][2] = x
			self.args[-1][3] = y
			self.host.on_move(self)
	
	def release(self, destroy=False):
		for key, value in self.cursor.save_state.items():
			self.cursor.save_state[key] = getattr(self.host, key, value)

		self.cursor.handle = None
		if destroy:
			self.host.on_destroy(self)
			self.cursor.auto_supply = False
		else:
			self.cursor.env.add_handle(self.host)
			if self.cursor.auto_supply:
				new_attachable = self.host.__class__()
				self.cursor.attach(new_attachable)


class Attachable(Drawable):
	def __init__(self, device):
		Drawable.__init__(self)
		self.device = device()

	def get_id(self):
		return self.device.get_id()

	def on_create(self, handle):
		pass
	def on_destroy(self, handle):
		pass
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
	def on_hand_over(self, button, press, x, y, cursor):
		if button==3 and not press:
			cursor.attach(self, apply_state=False)
	def on_update(self):
		pass

	def description(self):
		return self.device.description()

	def __repr__(self):
		return f"{self.device}_H"
