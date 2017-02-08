#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''

import shell_server
from testagent import cmd_HAagent
from testagent import file


"""
check is cluster in HAagent
:param cluster_name : cluster name
:param parser is a dict get from base.configure
"""

def is_cluster_exist(cluster_name , parser):
    ssh = shell_server.get_ssh(parser["NFS_ip"],
                               parser["NFS_usr"] , 
                               parser["NFS_pwd"]) # get ssh object
    cmd = cmd_HAagent.overview_cmd()
    s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd)
    
    overview = s_stdout.read()
    cluster_file_content = file.get_file_content(parser["cluster_file_path"])
    primary_node_file_content = file.get_file_content("%s%s.txt" % (parser["node_files_folder_path"] , parser["HostOS_ip"]))
    backup_node_file_content = file.get_file_content("%s%s.txt" % (parser["node_files_folder_path"] , parser["BackupOS_ip"]))
    
    print cluster_file_content
    print primary_node_file_content
    print backup_node_file_content
    
    ssh.close()

    if cluster_name in overview and cluster_file_content and primary_node_file_content and backup_node_file_content:
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
    