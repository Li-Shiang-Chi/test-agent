#!/usr/bin/python
#-*- coding: utf-8 -*-


'''
@author: lsc
'''


from testagent import preprocess
from testagent import process
from testagent import Assert


def run_HA3_non_primary_add_node(parser):
    preprocess.run_preprocess(parser)
    process.exec_non_primary_add_node(parser)
    Assert.detect_non_primary_node_add_node(parser)
    