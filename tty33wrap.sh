export TERM=tty33
export TERMCAP='tty33:bs:hc:os:xo:co#72:ht#8:bl=^G:cr=^M:do=^J:sf=^J:le=^H:
tty37:hd=\E9:hu=\E8:up=\E7:tc=tty33:'
export LS_COLORS=''
stty -echoe -echoke echoprt echok
# xcase is broken on linux, so iuclc makes it impossible to use uppercase
# unclear if olcuc is needed for tty-33. it doesn't translate {|}~ anyway.
if [ $# -gt 0 ]; then
	exec python3 throttle.py "$@"
else
	exec python3 throttle.py sh
fi
