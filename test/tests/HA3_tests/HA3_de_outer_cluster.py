#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''

from testagent import preprocess
from testagent import process
from testagent import Assert

def run_HA3_de_outer_cluster(parser):
    preprocess.run_preprocess(parser)
    process.exec_de_outer_cluster(parser)
    Assert.detect_de_outer_cluster(parser)