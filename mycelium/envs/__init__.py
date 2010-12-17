
try:
    import os
    if "/Users/skoczen/" == os.getcwd()[:15]:
        from dev import *
    else:
        from base import *
except:
    from base import *
