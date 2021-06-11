class Bit:
	def __init__(self, value=False):
		self.value = value

	def __bool__(self):
		return self.value

	def set(self, value, context):
		if value == self.value: return
		self.value = value
		self.on_change(value, context)
	
	def on_change(self, value, context):
		pass

	def __repr__(self):
		return f"Bit({self.value})"


class Dummy:
	def visit(self, context):
		pass
dummy = Dummy()

class Bridge(Bit):
	def __init__(self, device=None):
		Bit.__init__(self)
		self.connect(device)

	def connect(self, device=None):
		if device is None:
			device = dummy
		self.device = device

	def on_change(self, value, context):
		self.device.visit(context)

	def __repr__(self):
		return f"Bridge({self.value} -> {self.device.__class__.__name__})"


class Bus(Bit):
	def __init__(self):
		Bit.__init__(self)
		self.inputs = set()
		self.outputs = set()

	def on_change(self, value, context):
		for device in self.outputs:
			device.visit(context)

	def visit(self, context):
		self.set(any(self.inputs), context)

	def add_input(self, device):
		self.inputs.add(device)
	def add_output(self, device):
		self.outputs.add(device)
	
	def remove_input(self, device):
		self.inputs.remove(device)
	def remove_output(self, device):
		self.outputs.remove(device)

	def __repr__(self):
		return f"Bus({list(self.inputs)} -> {list(self.outputs)})"
