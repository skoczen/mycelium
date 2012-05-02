import os
import sys
try:
    if os.environ.has_key('DATABASE_URL'):
        from envs.live import *
    else:
        from envs.dev import *
except:
    print "Unexpected error:", sys.exc_info()