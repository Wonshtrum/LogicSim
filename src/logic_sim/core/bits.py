from ..utils import ID


class Named:
	def __repr__(self):
		return f"{self.__class__.__name__}_{ID(self)}"


class Visitable(Named):
	def visit(self, context):
		context.stage(self)

	def update(self, context):
		pass


class Dummy(Visitable):
	def __repr__(self):
		return "..."
DUMMY = Dummy()


class Bit:
	def __init__(self, owner=DUMMY, value=False, pin=None):
		self.owner = owner
		self.value = value
		self.drive = False
		self.pin = pin

	def __bool__(self):
		return self.value
	
	def __repr__(self):
		if self.pin is None:
			return f"{+self.value}{+self.drive} <- {self.owner}"
		return f"{+self.value}{+self.drive} <- {self.owner}_{self.pin}"


class Bridge:
	def __init__(self, A, B=DUMMY, pin_A=None, pin_B=None):
		self.A = Bit(A, pin=pin_A)
		self.B = Bit(B, pin=pin_B)

	def set(self, value, context, reverse=False):
		value = bool(value)
		A, B = (self.B, self.A) if reverse else (self.A, self.B)
		visit = value != A.drive
		if value:
			A.drive = True
			A.value = True
		else:
			A.drive = False
			A.value = self.B.drive
		if visit:
			B.owner.visit(context)

	def connect(self, device):
		self.B = Bit(device)
	
	def reverse(self):
		b = Bridge(DUMMY)
		b.A = self.B
		b.B = self.A
		return b

	def __bool__(self):
		return bool(self.B)

	def __repr__(self):
		return f"{+self.A.value}{+self.A.drive}-{self.B}"
