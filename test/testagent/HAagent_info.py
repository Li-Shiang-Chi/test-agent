#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''

import shell_server
import cmd_HAagent
import file
import json
from tkinter.tix import Shell



def is_add_primary_success(parser):
    """
    check is primary node add in cluster
    :param parser is a dict get from base.configure
    """
    is_exists = is_node_exists(parser["Cluster_name"], parser["HostOS_name"], parser) 
    role = get_node_role(parser["HostOS_name"], parser)
    
    print is_exists
    print role
    
    print "primary node is exists %s" % is_exists
    print "primary role %s (expeceted 0)" % role
    
    if is_exists and role == 0: # if node exists and the role equals 0(primary)
        return True
    return False

def is_add_backup_success(parser):
    """
    check is backup node add in cluster
    :param parser is a dict get from base.configure
    """
    is_exists = is_node_exists(parser["Cluster_name"], parser["BackupOS_name"], parser) 
    role = get_node_role(parser["BackupOS_name"], parser)
    
    print "backup node is exists %s" % is_exists
    print "backup role %s (expeceted 1)" % role
    
    if is_exists and role == 1: # if node exists and the role equals 1(backup)
        return True
    return False


def is_add_slave_success(parser):
    """
    check is slave node add in cluster
    :param parser is a dict get from base.configure
    """
    is_exists = is_node_exists(parser["Cluster_name"], parser["SlaveOS_name"], parser) 
    role = get_node_role(parser["SlaveOS_name"], parser)
    
    print "slave node is exists %s" % is_exists
    print "slave role %s (expeceted 2)" % role
    
    if is_exists and role == 2: # if node exists and the role equals 2(slave)
        return True
    return False

def is_cluster_exist(cluster_name , parser):
    """
    check is cluster in HAagent
    :param cluster_name : cluster name
    :param parser is a dict get from base.configure
    """
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
    ssh = shell_server.get_ssh(parser["HostOS_ip"],
                               parser["HostOS_usr"], 
                               parser["HostOS_pwd"]) # get ssh object
    cmd = cmd_HAagent.overview_cmd()
    s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd)
    
    overview = s_stdout.read() # get overview in host terminal
    
    ssh = shell_server.get_ssh(parser["NFS_ip"],
                               parser["NFS_usr"], 
                               parser["NFS_pwd"])
    cluster_file_content = file.get_remote_file_content(parser["cluster_file_path"] ,ssh) # get cluster file content in nfs
    
    print overview
    print cluster_file_content
    
    ssh.close()
    
    if node_name in overview and cluster_file_content:
        return True
    return False

def get_node_role(name , parser):
    ssh = shell_server.get_ssh(parser["NFS_ip"],
                               parser["NFS_usr"], 
                               parser["NFS_pwd"])
    
    cluster_file_content = file.get_remote_file_content(parser["cluster_file_path"] , ssh) # get cluster file content in nfs
    res = json.load(cluster_file_content)["nodes"][name]["role"] # get role 
    print res
    return res # return role

if  __name__ == '__main__':
    cluster_file_content = file.get_file_content("/var/ha/images/clusterFile.txt")
    jsonString = json.loads(cluster_file_content)
    print jsonString["nodes"]["n1"]["role"]
    print jsonString["nodes"]["n1"]["role"] == 0
     
    