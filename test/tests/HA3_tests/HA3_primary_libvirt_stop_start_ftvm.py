#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''

from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_HA3_primary_libvirt_stop_start_ftvm(parser):
    preprocess.run_preprocess(parser)
    process.stop_libvirt_process(parser)
    Assert.libvirt_stop_start_ftvm(parser)
    