#!/usr/bin/python env
#-*- coding: utf-8 -*-

'''

@author: lsc
'''

"""
get command in list
input :(String) command : input command
output :(list) command list
"""

def cmd(command):
    return command.split()



"""
get instruction with new line
input : command
output : command + new line
"""

def exec_cmd(command):
    return command+"\n"