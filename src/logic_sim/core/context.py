class Context:
	def __init__(self, name="unnamed context"):
		self.staged = set()
		self.visited = set()
		self.name = name
	
	def stage(self, device):
		print(self.name, "staged", device)
		self.trigger(device)
		self.staged.add(device)

	def visit(self, *devices):
		for device in devices:
			device.visit(self)

	def trigger(self, device):
		self.visited.add(device.get_id())

	def update(self):
		staged = self.staged
		self.staged = set()
		self.visited = set()
		for device in staged:
			device.update(self)
