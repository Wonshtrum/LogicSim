class Visitable:
	def visit(self, context):
		context.stage(self)

	def update(self, context):
		pass


class Dummy(Visitable):
	def __repr__(self):
		return "..."
DUMMY = Dummy()


class Bit:
	def __init__(self, owner=DUMMY, value=False):
		self.value = value
		self.drive = False
		self.owner = owner

	def __bool__(self):
		return self.value
	
	def __repr__(self):
		return f"{+self.value}{+self.drive} <- {self.owner}"


class Bridge:
	def __init__(self, A, B=DUMMY):
		self.A = Bit(A)
		self.B = Bit(B)

	def set(self, value, context):
		visit = value != self.A.drive
		if value:
			self.A.drive = True
			self.A.value = True
		else:
			self.A.drive = False
			self.A.value = self.B.drive
		if visit:
			self.B.owner.visit(context)
	
	def reverse(self):
		b = Bridge(DUMMY)
		b.A = self.B
		b.B = self.A
		return b

	def __bool__(self):
		return bool(self.B)

	def __repr__(self):
		return f"{+self.A.value}{+self.A.drive}-{self.B}"
