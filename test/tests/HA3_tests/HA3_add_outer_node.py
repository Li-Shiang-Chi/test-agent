
#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''


from testagent import preprocess
from testagent import process
from testagent import Assert

def run_HA3_add_outer_node(parser):
    preprocess.run_preprocess(parser)
    process.exec_add_outer_node(parser)
    Assert.detect_add_outer_node(parser)