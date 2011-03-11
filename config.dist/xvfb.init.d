#!/bin/bash
#
# /etc/rc.d/init.d/xvfb
#
# chkconfig: 345 98 90
# description: starts virtual framebuffer process to
# enable server
#
#
#
# Source function library.
#.  /etc/init.d/functions
XVFB_OUTPUT=/tmp/Xvfb.out
XVFB=/usr/bin/Xvfb
XVFB_OPTIONS=":5 -screen 0 1024x768x24 -fbdir /var/run"

start()  {
echo -n "Starting : X Virtual Frame Buffer "
$XVFB $XVFB_OPTIONS >>$XVFB_OUTPUT 2>&1&
RETVAL=$?
echo
return $RETVAL
}

stop()   {
echo -n "Shutting down : X Virtual Frame Buffer"
echo
killall Xvfb
echo
return 0
}

case "$1" in
start)
start
;;
stop)
stop
;;
status)
status xvfb
;;
restart)
    stop
    start
    ;;

*)
echo "Usage: xvfb {start|stop|status|restart}"
exit 1
;;
esac
exit $?
