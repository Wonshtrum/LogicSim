from .handles import Chip
from ..utils import super_init
from ..devices import *


@super_init(And, 3, 2, [1,0,1,0,1,0])
class Chip_And(Chip):
	pass
