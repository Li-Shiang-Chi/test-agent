#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''

import shell_server
import cmd_HAagent
import file
import json


"""
check is cluster in HAagent
:param cluster_name : cluster name
:param parser is a dict get from base.configure
"""

def is_backup_success(parser):
    return False

def is_cluster_exist(cluster_name , parser):
    ssh = shell_server.get_ssh(parser["NFS_ip"],
                               parser["NFS_usr"] , 
                               parser["NFS_pwd"]) # get ssh object
    cmd = cmd_HAagent.overview_cmd()
    s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd)
    
    overview = s_stdout.read()
    cluster_file_content = file.get_file_content(parser["cluster_file_path"])
    
    ssh.close()

    if cluster_name in overview and cluster_file_content:
        return True
    return False

"""
check is node in HAagent
:param cluster_name : cluster name
:param node_name : node name
:param parser : is a dict get from base.configure
"""

def is_node_exists(cluster_name , node_name , parser):
    ssh = shell_server.get_ssh(parser["NFS_ip"],
                               parser["NFS_usr"] , 
                               parser["NFS_pwd"]) # get ssh object
    cmd = cmd_HAagent.overview_cmd()
    s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd)
    
    overview = s_stdout.read()
    cluster_file_content = file.get_file_content(parser["cluster_file_path"])
    
    ssh.close()
    
    if node_name in overview and cluster_file_content:
        return True
    return False

def get_node_role(ip , parser):
    return False

if  __name__ == '__main__':
    cluster_file_content = file.get_file_content("/var/ha/images/clusterFile.txt")
    jsonString = json.loads(cluster_file_content , ensure_ascii = False)
    print jsonString
     
    