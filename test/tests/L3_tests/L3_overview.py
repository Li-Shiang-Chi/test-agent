#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''

from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L3_overview(parser):
    preprocess.run_preprocess(parser)
    process.exec_overview(parser)
    Assert.detect_overview(parser)
    postprocess.run_postprocess(parser)