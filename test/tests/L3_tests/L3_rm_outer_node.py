
#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''


from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess


#not implement

def run_L3_de_outer_node(parser):
    preprocess.run_preprocess(parser)
    process.exec_de_outer_node(parser)
    Assert.detect_de_outer_node(parser)
    postprocess.run_postprocess(parser)