
#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''


from testagent import preprocess
from testagent import process
from testagent import Assert

def run_L3_add_duplicate_node(parser):
    preprocess.run_preprocess(parser)
    process.exec_add_duplicate_node(parser)
    Assert.detect_add_duplicate_node(parser)