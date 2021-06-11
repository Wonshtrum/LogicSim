class Context:
	def __init__(self, name="unnamed context"):
		self.staged = set()
	
	def stage(self, device):
		print("staged", device)
		self.staged.add(device)

	def update(self):
		staged = self.staged
		self.staged = set()
		for device in staged:
			device.update(self)
