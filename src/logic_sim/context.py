class Context:
	def __init__(self, name="unnamed context"):
		self.staged = set()
		self.name = name
	
	def stage(self, device):
		print(self.name, "staged", device)
		self.staged.add(device)

	def visit(self, device):
		device.visit(self)

	def update(self):
		staged = self.staged
		self.staged = set()
		for device in staged:
			device.update(self)
