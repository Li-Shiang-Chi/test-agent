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

def compile_command(command):
    return command.split()



"""
get instruction with new line
input : command
output : command + new line
"""

def exec_command(command):
    return command+"\n"