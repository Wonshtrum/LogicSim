from utils import super_init
from connectics import *


class Gate:
	def __init__(self, n_inputs=2, n_outputs=1):
		self.n_inputs = n_inputs
		self.n_outputs = n_outputs
		self.n_pins = n_inputs+n_outputs
		self.inputs = [Bridge(self) for _ in range(n_inputs)]
		self.outputs = [Bridge() for _ in range(n_outputs)]

	def connect(self, bus, pin):
		if pin < self.n_inputs:
			bridge = self.inputs[pin]
			bus.add_output(bridge)
		else:
			bridge = self.outputs[pin-self.n_inputs]
			bridge.connect(bus)
			bus.add_input(bridge)

	def visit(self, context):
		context.stage(self)

	def update(self, context):
		pass

	def __repr__(self):
		return f"{self.__class__.__name__}({self.inputs} -> {self.outputs})"


@super_init(1, 1)
class Not(Gate):
	def update(self, context):
		in_0, = self.inputs
		out_0, = self.outputs
		out_0.set(not in_0, context)
		print(self)

@super_init(2, 1)
class And(Gate):
	def update(self, context):
		in_0, in_1 = self.inputs
		out_0, = self.outputs
		out_0.set(in_0 and in_1, context)
		print(self)

@super_init(2, 1)
class Or(Gate):
	def update(self, context):
		in_0, in_1 = self.inputs
		out_0, = self.outputs
		out_0.set(in_0 or in_1, context)
		print(self)

@super_init(2, 1)
class Xor(Gate):
	def update(self, context):
		in_0, in_1 = self.inputs
		out_0, = self.outputs
		out_0.set(in_0 ^ in_1, context)
		print(self)
