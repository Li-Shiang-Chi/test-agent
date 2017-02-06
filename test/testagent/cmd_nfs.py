#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
@author: lsc
'''
def clear_cluster_file(parser):
    return "sudo rm" % (parser["cluster_file_path"])
def clear_node_files(parser):
    return "sudo rm -rf" % (parser["primary_node_file_path"])