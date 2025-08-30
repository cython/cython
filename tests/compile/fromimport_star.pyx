# mode: compile

from spam import *
from ...spam.foo import *
from ... spam.foo import *
from .. . spam.foo import *
from . . . spam.foo import *
from . .. spam.foo import *
from . import *
from ... import *
from .. . import *
from . .. import *
from . . . import *
