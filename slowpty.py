#!/usr/bin/env python3
"Simple script to reduce output speed."
# Doing it inside the terminal emulator alone causes serious problems for
# non-pty backends. This allows e.g. interrupting a long output to work more
# like how it would have on classic systems. Works in WSL and Mac, but not
# Linux. There seems to be no way to get nice behavior at all on Linux.

import pty
import os
import select
import time
import sys
import termios
import tty

# pylint: disable=invalid-name,protected-access,broad-except
def main():
    "Main function"
    attr = termios.tcgetattr(0)
    pid, fd = pty.fork()
    cmd = sys.argv[1:] or ['sh']
    CHARS_PER_SEC = 10
    CHAR_DELAY = 1/CHARS_PER_SEC
    if pid == 0:
        try:
            attr[4] = attr[5] = termios.B110
            termios.tcsetattr(0, termios.TCSAFLUSH, attr)
            os.execvp(cmd[0], cmd)
        except Exception as e:
            print(e)
            os._exit(126)
        os._exit(126)

    tty.setraw(0)
    try:
        while True:
            rl = select.select((0, fd), (), ())[0]
            if 0 in rl:
                data = os.read(0, 64)
                os.write(fd, data)
            if fd in rl:
                data = os.read(fd, 1)
                os.write(1, data)
                time.sleep(0.1)
    finally:
        termios.tcsetattr(0, termios.TCSAFLUSH, attr)

main()
