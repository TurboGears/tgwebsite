import os
import sys

sys.stdout = sys.stderr
os.environ['PYTHON_EGG_CACHE'] = '/home/turbogearsorg/tracvenv/traceggs'
os.environ['TRAC_ENV'] = '/home/turbogearsorg/tracvenv'

import trac.web.main

application = trac.web.main.dispatch_request
