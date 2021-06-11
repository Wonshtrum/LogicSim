def super_init(*args, **kwargs):
	def decorator(cls):
		old_init = cls.__init__
		if old_init is cls.__base__.__init__:
			old_init = lambda *args, **kwargs: None
		def __init__(self, *_args, **_kwargs):
			cls.__base__.__init__(self, *args, **kwargs)
			old_init(self, *_args, **_kwargs)
		cls.__init__ = __init__
		return cls
	return decorator
