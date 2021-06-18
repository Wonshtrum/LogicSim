class Handle:
	def __init__(self, host, cursor):
		self.host = host
		self.cursor = cursor
		self.args = [[None, None, cursor.x, cursor.y]]
		host.on_create(self)

	def button(self, num, press, x, y):
		head = self.args.pop()
		self.args.append([num, press, x, y])
		if self.host.on_button(self) is False:
			self.args.pop()
		self.args.append(head)

	def key(self, code):
		if code == 9 and len(self.args)>1:
			self.args.pop(-2)
		self.host.on_key(code, self)

	def move(self, x, y):
		if (x, y) != self.args[-1][2:]:
			self.args[-1][2] = x
			self.args[-1][3] = y
			self.host.on_move(self)
	
	def release(self, destroy=False):
		self.cursor.handle = None
		if destroy:
			self.host.on_destroy(self)
		else:
			self.cursor.env.add_handle(self.host)


class Attachable:
	def __init__(self, device):
		self.device = device()

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
	
	def __repr__(self):
		return f"{self.device}_H"
