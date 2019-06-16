#!/usr/bin/python
import subprocess

def shell(*args):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    out, err = proc.communicate()
    return out, err
