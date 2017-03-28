#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
@author: lsc
'''
def clear_cluster_file(parser):
    print "sudo rm %s" % (parser["cluster_file_path"])
    return "sudo rm %s" % (parser["cluster_file_path"])
def clear_node_files(parser):
    print "sudo rm -rf %s" % (parser["node_files_folder_path"])
    return "sudo rm -rf %s" % (parser["node_files_folder_path"])