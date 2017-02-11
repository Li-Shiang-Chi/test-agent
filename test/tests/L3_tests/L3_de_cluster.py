
#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
@author: lsc
'''

from testagent import preprocess
from testagent import process
from testagent import Assert

def run_L3_de_cluster(parser):
    preprocess.run_preprocess(parser)
    process.exec_de_cluster(parser)
    Assert.detect_de_cluster(parser)
    