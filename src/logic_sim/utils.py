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


def ID(obj):
	i = id(obj)*2654435761%(2**32)
	return "".join(chr(65+(i>>(8*j))%26) for j in range(4))


def desc(obj):
	if hasattr(obj, "description"):
		print(obj.description())
	else:
		print(obj)

def bind(func, *args, **kwargs):
	return lambda *_, **__: func(*args, *_, **kwargs, **__)
