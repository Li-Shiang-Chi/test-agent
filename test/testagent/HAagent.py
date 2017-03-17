#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
@author: lsc
'''


import cmd_HAagent
import cmd_egrep
import subprocess
import cmd


"""
    execute createcluster <cluster name> <node name> (ibmp) (shelf ip)
    :param cluster_name: host cluster name
    :param node_name: node name
    :param ibmp: ibmp
    :param shelf_ip: shelf_ip
    :return: succuess / fail
    """
def create_cluster(cluster_name , node_name , ibmp , shelf_ip , parser=None , ssh=None):
    cmd = cmd_HAagent.create_cluster_cmd(cluster_name, node_name, ibmp, shelf_ip)
    return remote_exec(cmd, ssh) if ssh else local_exec(cmd, parser)

    """
    execute decluster <cluster name>

    :param cluster_name: host cluster name
    :return: succuess / fail
    """
def de_cluster(cluster_name , parser=None , ssh=None):
    cmd = cmd_HAagent.de_cluster_cmd(cluster_name)
    return remote_exec(cmd, ssh) if ssh else local_exec(cmd, parser)
    
    """
    execute addnode <cluster name> <node name> <node ip> (ibmp)

    :param cluster_name: host cluster name
    :param node_name: node name
    :param node_ip: node_ip
    :return: succuess / fail
    """
def add_node(cluster_name , node_name , node_ip , ibmp , parser=None , ssh=None):
    cmd = cmd_HAagent.add_node_cmd(cluster_name, node_name, node_ip, ibmp)
    return remote_exec(cmd, ssh) if ssh else local_exec(cmd, parser)

def add_backup_node(parser , ssh):
    add_node(parser["Cluster_name"],
             parser["BackupOS_name"], 
             parser["BackupOS_ip"], 
             parser["BackupOS_ipmb"], 
             parser, ssh)
def add_slave_node(parser , ssh):
    add_node(parser["Cluster_name"],
             parser["SlaveOS_name"], 
             parser["SlaveOS_ip"], 
             parser["SlaveOS_ipmb"], 
             parser,ssh)
    
    """
    execute rmnode <cluster name> <node name>

    :param cluster_name: host cluster name
    :param node_name: node name
    :return: succuess / fail
    """
def rm_node(cluster_name , node_name , parser=None , ssh=None):
    cmd = cmd_HAagent.rm_node_cmd(cluster_name, node_name)
    return remote_exec(cmd, ssh) if ssh else local_exec(cmd, parser)
    """
    execute startftvm <node name> <vm name> <xml path>

    :param node_name: node name
    :param vm_name: vm_name
    :param xml_path: xml_path
    :return: succuess / fail
    """
def start_ftvm(node_name , vm_name , xml_path=None , parser=None , ssh=None):
    cmd = cmd_HAagent.start_ftvm_cmd(node_name, vm_name, xml_path)
    print cmd
    return remote_exec(cmd, ssh) if ssh else local_exec(cmd, parser)
    """
    execute removeftvm <vm name>

    :param vm_name: vm_name
    :return: succuess / fail
    """

def remove_ftvm(vm_name , parser=None , ssh=None):
    cmd = cmd_HAagent.remove_ftvm_cmd(vm_name)
    return remote_exec(cmd, ssh) if ssh else local_exec(cmd, parser)
    """
    execute overview
    :return: information about the whole system
    """
def overview(parser=None , ssh=None):
    cmd = cmd_HAagent.overview_cmd()
    return remote_exec(cmd, ssh) if ssh else local_exec(cmd, parser)
    """
    execute exit
    :return: exit the HAagent
    """
def exit(parser=None , ssh=None):
    cmd = cmd_HAagent.exit_cmd()
    return remote_exec(cmd, ssh) if ssh else local_exec(cmd, parser)

    """
    local side execute using subprocess module
    :param cmd: command
    :param parser: system configuration
    :return: execute the command
    """

def local_exec(cmd , parser):
    p = subprocess.Popen(cmd.split() ,stdin=subprocess.PIPE , shell=False)
    return p.communicate()
    """
    remote side execute using ssh module
    :param cmd: command
    :return: execute the command
    """
def remote_exec(cmd , ssh=None):
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
    stdout = s_stdout.read()
    print stdout.rstrip()
    return stdout.rstrip()