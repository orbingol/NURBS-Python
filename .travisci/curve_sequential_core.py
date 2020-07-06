# Performance testing on the TravisCI
import os
import sys
import platform
import timeit
from geomdl.core import NURBS, knotvector


# Setup test
def setup_test():
    ctrlpts = [[5.0, 15.0, 0.0], [10.0, 25.0, 5.0], [20.0, 20.0, 10.0], [15.0, -5.0, 15.0], [7.5, 10.0, 20.0],
               [12.5, 15.0, 25.0], [15.0, 0.0, 30.0], [5.0, -10.0, 35.0], [10.0, 15.0, 40.0], [5.0, 15.0, 30.0]]

    ns = NURBS.Curve()
    ns.degree = [3]
    ns.set_ctrlpts(ctrlpts)
    ns.knotvector = [knotvector.generate(ns.degree.u, ns.ctrlpts_size.u)]
    ns.sample_size = 16384

    return ns


# Setup number of executions
number = os.environ['GEOMDL_PERF_NUMBER'] if 'GEOMDL_PERF_NUMBER' in os.environ else 50
repeat = os.environ['GEOMDL_PERF_REPEAT'] if 'GEOMDL_PERF_REPEAT' in os.environ else 3
version = os.environ['TRAVIS_PYTHON_VERSION'] if 'TRAVIS_PYTHON_VERSION' in os.environ else ".".join(str(v) for v in sys.version_info[0:3])

# Run timeit
res = timeit.repeat(setup="from __main__ import setup_test; ns=setup_test()", stmt="ns.evaluate()",
                    repeat=repeat, number=number)

# Print results
print(__file__, "on", platform.python_implementation(), str(version), ">>", str(number), "loops, best of", str(repeat), "is", str(min(res)), "seconds per loop")
