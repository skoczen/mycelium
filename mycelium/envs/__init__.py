
try:
    import os
    if "/Users/skoczen/" == os.getcwd()[:15]:
        print "foo"
        from dev import *
except:
    from base import *

    import traceback
    import sys
    print "######################## Exception #############################"
    print '\n'.join(traceback.format_exception(*sys.exc_info()))
    print "################################################################"

    print "act"
    pass