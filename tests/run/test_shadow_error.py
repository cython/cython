# mode: run
# tag: numpy, gh5411

import pickle
import numpy as np

# This adds e.g
# sys.modules['cython.cimports'] = CythonCImports('cython.cimports')
from Cython import Shadow

# This calls hasattr(CythonCImports, "add")
add = pickle.loads(pickle.dumps(np.add))

assert add is np.add
