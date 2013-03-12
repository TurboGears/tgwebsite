import sys
sys.stdout = sys.stderr

import site 
site.addsitedir('/home/turbogearsorg/tracvenv/lib/python2.6/site-packages')

import os
os.environ['PYTHON_EGG_CACHE'] = '/home/turbogearsorg/tracvenv/traceggs'
os.environ['TRAC_ENV'] = '/home/turbogearsorg/tracvenv/project'

import trac.web.main

application = trac.web.main.dispatch_request
