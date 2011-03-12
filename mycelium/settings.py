import os
try:
    cwd = "%s" % (os.getcwd(),)
    if "/Users/skoczen/" == cwd[:15]:
        from envs.dev import *
except:
    pass