from .bits import *
from .utils import *


class Gate(Visitable):
	def __init__(self, n_pins=4):
		self.n_pins = n_pins
		self.pins = [Bridge(self, pin_A=pin) for pin in range(n_pins)]
	
	def connect(self, pin, bridge):
		pin = self.pins[pin]
		pin.B = bridge.A
		bridge.B = pin.A
	
	def clone(self):
		return self.__class__(self.n_pins)
	
	def __getitem__(self, pin):
		return self.pins[pin]

	def description(self):
		return f"{self}"+"".join(f"\n  {pin}" for pin in self.pins)


@super_init(2)
class Not(Gate):
	def update(self, context):
		pin_0, pin_1 = self.pins
		pin_1.set(not pin_0, context)

@super_init(3)
class And(Gate):
	def update(self, context):
		pin_0, pin_1, pin_2 = self.pins
		pin_2.set(pin_0 and pin_1, context)

@super_init(3)
class Or(Gate):
	def update(self, context):
		pin_0, pin_1, pin_2 = self.pins
		pin_2.set(pin_0 or pin_1, context)

@super_init(3)
class Xor(Gate):
	def update(self, context):
		pin_0, pin_1, pin_2 = self.pins
		pin_2.set(pin_0 ^ pin_1, context)

@super_init(3)
class Nand(Gate):
	def update(self, context):
		pin_0, pin_1, pin_2 = self.pins
		pin_2.set(not(pin_0 and pin_1), context)

@super_init(3)
class Nor(Gate):
	def update(self, context):
		pin_0, pin_1, pin_2 = self.pins
		pin_2.set(not(pin_0 or pin_1), context)
