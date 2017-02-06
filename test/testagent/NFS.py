#!/usr/bin/python
#-*- coding: utf-8 -*-

"""
@author :lsc
"""

import cmd_nfs
import sub_process
from testagent import TA_error


def checkIsFileCleared(parser , ssh = None):
    if ssh:
        checkIsClusterFileCleared(parser, ssh)
        checkIsPrimaryNodeFileCleared(parser, ssh)
        checkIsBackupNodeFileCleared(parser, ssh)
        #checkIsSlaveNodeFileCleared(parser, ssh)
    else:
        raise TA_error.Preprocess_Error("not getting nfs shell server")
        
        
def checkIsClusterFileCleared(parser , ssh = None):
    cmd = "cat %s" % parser["cluster_file_path"]
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
    if s_stdout != "":
        raise TA_error.Preprocess_Error("nfs file not cleared")
    else:
        return True
def checkIsPrimaryNodeFileCleared(parser , ssh = None):
    cmd = "ls %s" % parser["primary_node_file_path"]
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
    expected = "%s.txt" % parser["HostOS_ip"]
    if s_stdout == expected: #file exist
        cmd = "cat %s" % parser["primary_node_file_path"]
        s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
        if s_stdout == "": #check file is cleared
            return True
        raise TA_error.Preprocess_Error("primary node file not cleared")
    
def checkIsBackupNodeFileCleared(parser , ssh = None):
    cmd = "ls %s" % parser["backup_node_file_path"]
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
    expected = "%s.txt" % parser["BackupOS_ip"]
    if s_stdout == expected: #file exist
        cmd = "cat %s" % parser["backup_node_file_path"]
        s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
        if s_stdout == "": #check file is cleared
            return True
        raise TA_error.Preprocess_Error("backup node file not cleared")
    
def checkIsSlaveNodeFileCleared(parser , ssh = None):
    cmd = "ls %s" % parser["slave_node_file_path"]
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
    expected = "%s.txt" % parser["SlaveOS_ip"]
    if s_stdout == expected: #file exist
        cmd = "cat %s" % parser["slave_node_file_path"]
        s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
        if s_stdout == "": #check file is cleared
            return True
        raise TA_error.Preprocess_Error("slave node file not cleared")

def clear_cluster_file(parser , ssh=None):
    cmd = cmd_nfs.clear_cluster_file(parser)
    return remote_exec(cmd , ssh) if ssh else local_exec(cmd ,parser)

def clear_node_files(parser , ssh=None):
    cmd = cmd_nfs.clear_node_files(parser)
    return remote_exec(cmd , ssh) if ssh else local_exec(cmd ,parser)
        
def reset(parser , ssh = None):
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
    