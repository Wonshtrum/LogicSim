from bits import *
from utils import *


class Gate(Visitable):
	def __init__(self, n_pins=4):
		self.n_pins = n_pins
		self.pins = [Bridge(self) for _ in range(n_pins)]
	
	def connect(self, pin, bridge):
		pin = self.pins[pin]
		pin.B = bridge.A
		bridge.B = pin.A
	
	def __getitem__(self, pin):
		return self.pins[pin]
	
	def __repr__(self):
		return f"{self.__class__.__name__}_{ID(self)}"

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
