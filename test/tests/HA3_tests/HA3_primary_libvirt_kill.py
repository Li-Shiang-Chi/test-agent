#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''

from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_HA3_primary_libvirt_kill(parser):
    preprocess.run_preprocess(parser)
    process.kill_libvirt_process(parser)
    Assert.FTsystem_running_in_hostOS(parser)