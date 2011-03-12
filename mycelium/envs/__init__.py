import os
try:
    cwd = "%s" % (os.getcwd(),)
    if "/Users/skoczen/" == cwd[:15]:
        from dev import *
    else:
        raise "Settings not specified"
except:
    from qi_toolkit.helpers import print_exception
    print "Excepted"
    print_exception()
    from dev import *
