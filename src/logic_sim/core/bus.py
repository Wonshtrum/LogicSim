from .bits import *


class Bus(Visitable):
	def __init__(self):
		self.connections = set()
		self.value = False

	def connect(self, bridge):
		bridge.connect(self)
		self.connections.add(bridge)
	
	def visit(self, context):
		context.trigger(self)
		sources = [connection for connection in self.connections if connection.A.drive]
		unique = len(sources)==1
		self.value = bool(sources)
		for connection in self.connections:
			connection.set(self.value and (not unique or connection not in sources), context, reverse=True)

	def __getitem__(self, connection):
		return list(self.connections)[connection]

	def description(self):
		return f"{self}"+"".join(f"\n  {connection.reverse()}" for connection in self.connections)
