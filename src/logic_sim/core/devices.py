from .gates import *


class Device(Gate):
	def __call__(self):
		return self.clone()

	def clone(self):
		raise NotImplementedError
