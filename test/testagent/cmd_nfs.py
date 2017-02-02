#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
@author: lsc
'''


def clear_cluster_file(parser):
    return "truncate -s 0 %s" % (parser["cluster_file_path"])

def clear_primary_node_file(parser):
    return "truncate -s 0 %s" % (parser["primary_node_file_path"])

def clear_backup_node_file(parser):
    return "truncate -s 0 %s" % (parser["backup_node_file_path"])