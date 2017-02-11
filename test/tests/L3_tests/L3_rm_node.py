
#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''


from testagent import preprocess
from testagent import process
from testagent import Assert

def run_L3_rm_node(parser):
    preprocess.run_preprocess(parser)
    process.exec_de_node(parser)
    Assert.detect_de_node(parser)