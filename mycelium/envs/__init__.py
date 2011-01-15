try:
    import os
    cwd = "%s" % (os.getcwd(),)
    if "/Users/skoczen/" == cwd[:15]:
        from dev import *
    else:
        if cwd.find("staging") != -1:
            from staging import *
        else:
            from live import *
except:
    from live import *
