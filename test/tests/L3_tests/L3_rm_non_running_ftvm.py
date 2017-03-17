
#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''


from testagent import preprocess
from testagent import process
from testagent import Assert

def run_L3_rm_non_running_ftvm(parser):
    preprocess.run_preprocess(parser)
    Assert.rm_non_running_ftvm(parser)