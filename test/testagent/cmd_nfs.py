#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
@author: lsc
'''
def clear_cluster_file(parser):
    return "sudo rm %s" % (parser["cluster_file_path"])
def clear_node_files(parser):
    return "sudo rm -rf %s" % (parser["primary_node_file_path"])