from .bits import *


class Bus(Visitable):
	def __init__(self):
		self.connections = set()

	def connect(self, bridge):
		print(bridge)
		bridge.connect(self)
		self.connections.add(bridge)
	
	def visit(self, context):
		sources = [connection for connection in self.connections if connection.A.drive]
		unique = len(sources)==1
		value = bool(sources)
		for connection in self.connections:
			connection.set(value and (not unique or connection not in sources), context, reverse=True)

	def description(self):
		return f"{self}"+"".join(f"\n  {connection.reverse()}" for connection in self.connections)
