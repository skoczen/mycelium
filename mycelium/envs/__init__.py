
try:
    import os
    if "/Users/skoczen/" == os.getcwd()[:15]:
        print "foo"
        from dev import *
    else:
        from base import *
except:
    from base import *
