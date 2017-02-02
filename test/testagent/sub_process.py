#!/usr/bin/python
#-*- coding: utf-8 -*-
'''

@author: lsc
'''
import os
import signal
import command
import subprocess
import data_dir



"""
get subprocess obeject
input :None
output : subprocess object
"""

p = None

def get_sub_process(parser):
    global p
    if p != None: return
    compile_py = command.compile_command("sudo python " + parser["command_handler_path"])
    p = subprocess.Popen(compile_py  , stdin=subprocess.PIPE , shell=False , cwd=parser["current_work_dir"])
    return p

def close_sub_process(parser):
    global p
    if p == None : return
    os.kill(os.getpid(p.pid) , signal.SIGTERM)