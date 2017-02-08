#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
@author :lsc
"""

import cmd_nfs
import sub_process
import TA_error
from testagent import TA_error


def checkIsFileCleared(parser , ssh = None):
    if ssh:
        checkIsClusterFileCleared(parser, ssh)
        checkIsNodeFilesCleared(parser, ssh)
    else:
        raise TA_error.Preprocess_Error("not getting nfs shell server")
def checkIsClusterFileCleared(parser , ssh = None):
    cmd = "ls %s" % parser["local_nfs_path"]
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
    if "clusterFile.txt" in s_stdout.read():
        raise TA_error.Preprocess_Error("cluster file not cleared")
    else:
        return True
def checkIsNodeFilesCleared(parser , ssh = None):
    cmd = "ls %s" % parser["node_files_path"]
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
    expected = ""
    if s_stdout.read() == expected: #file not exist
        return True
    raise TA_error.Preprocess_Error("node files not cleared")

def clear_cluster_file(parser , ssh=None):
    cmd = cmd_nfs.clear_cluster_file(parser)
    return remote_exec(cmd , ssh) if ssh else local_exec(cmd ,parser)

def clear_node_files(parser , ssh=None):
    cmd = cmd_nfs.clear_node_files(parser)
    return remote_exec(cmd , ssh) if ssh else local_exec(cmd ,parser)
        
def reset(parser , ssh = None):
    if not ssh :
        raise TA_error.Shell_server_Error("not getting ssh")
    clear_cluster_file(parser, ssh)
    clear_node_files(parser, ssh)

def local_exec(cmd , parser):
    p = sub_process.get_sub_process(parser)
    cmd = cmd[len('mmsh'):] # remove mmsh string from cmd  
    p.stdin.write(cmd)
    return p.communicate()
    
    """
    remote side execute using ssh module
    :param cmd: command
    :return: execute the command
    """
def remote_exec(cmd , ssh=None):
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
    stdout = s_stdout.read()
    return stdout.rstrip()
    