#!/usr/bin/python
#-*- coding: utf-8 -*-
import paramiko
import sys
import time
import cmd_service
import cmd_egrep
import shell_server
import FTsystem
import FTVM
import FTOS
import master_monitor
import mmsh
import TA_error
import subprocess
import os
import HAagent
import NFS
from testagent import sub_process


"""
when test case start , preprocess will clear the cluster and node file(refresh system)
:param parser : is a dict , get from test config file
"""
def run_preprocess(parser):
    preprocess_Host(parser)
    preprocess_Backup(parser)
    #preprocess_Slave(parser)
    #preprocess_NFS(parser)
    
def preprocess_Host(parser):
    """
    when test case start host node do some preprocess
    :param parser : is a dict , get from test config file
    """
    
    ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh 
    preprocessHostOS(parser)
    preprocessHostMount(parser, ssh)
    
    ssh.close()
    
def preprocess_Backup(parser):
    """
    when test case start backup node do some preprocess
    :param parser : is a dict , get from test config file
    """
    ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh 
    preprocessBackupOS(parser)
    preprocessBackupMount(parser, ssh)
    ssh.close()
    
def preprocess_Slave(parser):
    """
    when test case start slave node do some preprocess
    :param parser : is a dict , get from test config file
    """
    ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh 
    preprocessSlaveOS(parser)
    preprocessSlaveMount(parser, ssh)
    ssh.close()

def preprocess_NFS(parser):
    ssh = shell_server.get_ssh(parser["NFS_ip"]
                              , parser["NFS_usr"]
                              , parser["NFS_pwd"]) #獲得ssh
    ssh.close()
    
def preprocessHostOS(parser):
    """
    preprocess  , Host os part , check Host node is booted
    :param parser : is a dict , get from test config file
    """
    if FTOS.HostOSIsRunning(parser) == False: # check node is running
        raise TA_error.Preprocess_Error("host os not booted") # node not running raise Error
def preprocessHostMount(parser , ssh):
    """
    preprocess , check Host node is mounting to nfs
    :param parser : is a dict , get from test config file
    """
    if preprocessIsHostOsMountNFS(parser , ssh) == False: # check node is mount to nfs
        preprocessHostOSMountNFS(parser , ssh) # mount to nfs
    if preprocessIsHostOsMountNFS(parser , ssh) == False: # re check node is mount to nfs
        raise TA_error.Preprocess_Error("Host os not mount to nfs") # not mount to nfs , raise error
    
    
def preprocessBackupOS(parser):
    """
    preprocess  , Host os part , check backup node is booted
    :param parser : is a dict , get from test config file
    """

    if FTOS.BackupOSIsRunning(parser) == False: # check node is running
        raise TA_error.Preprocess_Error("backup os not booted") # node not running raise error
def preprocessBackupMount(parser , ssh):
    """
    preprocess , check backup node is mounting to nfs
    :param parser : is a dict , get from test config file
    """
    if preprocessIsBackupOsMountNFS(parser , ssh) == False: # check node is mount to nfs
        preprocessBackUpOSMountNFS(parser , ssh) # mount to nfs
    if preprocessIsBackupOsMountNFS(parser , ssh) == False: # re check node is mount to nfs
        raise TA_error.Preprocess_Error("back up os not mount to nfs") # not mount to nfs , raise error
def preprocessSlaveOS(parser):
    """
    preprocess  , Host os part , check slave node is booted
    :param parser : is a dict , get from test config file
    """

    if FTOS.SlaveOSIsRunning(parser) == False:
        raise TA_error.Preprocess_Error("slave os not booted")
def preprocessSlaveMount(parser , ssh):
    """
    preprocess , slave Host node is mounting to nfs
    :param parser : is a dict , get from test config file
    """
    if preprocessIsSlaveOsMountNFS(parser , ssh) == False:
        preprocessSlaveOSMountNFS(parser , ssh)
    if preprocessIsSlaveOsMountNFS(parser , ssh) == False:
        raise TA_error.Preprocess_Error("slave os not mount to nfs")
    
def preprocessHostOSMountNFS(parser , ssh = None):
    cmd = "mount -t nfs %s:%s %s" % (parser["nfs_ip"],parser["nfs_share_folder"],parser["hostOS_mount_nfs_folder"])
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
    
def preprocessBackUpOSMountNFS(parser , ssh = None):
    cmd = "mount -t nfs %s:%s %s" % (parser["nfs_ip"],parser["nfs_share_folder"],parser["BackupOS_mount_nfs_folder"])
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
    
def preprocessSlaveOSMountNFS(parser , ssh = None):
    cmd = "mount -t nfs %s:%s %s" % (parser["nfs_ip"],parser["nfs_share_folder"],parser["SlaveOS_mount_nfs_folder"])
    s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
       
def preprocessIsHostOsMountNFS(parser , ssh = None):
    cmd = "ls %s" % parser["hostOS_mount_nfs_folder"]
    
    t_start = time.time()
    
    while (time.time() - t_start) < parser["pre_node_wait_mount_nfs_time"]: # use while loop to check , once mounted break the loop
        time.sleep(1) # check each sec
        s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
        if s_stdout != "":
            return True
    return False

def preprocessIsBackupOsMountNFS(parser , ssh = None):
    cmd = "ls %s" % parser["BackupOS_mount_nfs_folder"]
    
    t_start = time.time()
    
    while (time.time() - t_start) < parser["pre_node_wait_mount_nfs_time"]:
        time.sleep(1)
        s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
        if s_stdout != "":
            return True
    return False

def preprocessIsSlaveOsMountNFS(parser , ssh = None):
    cmd = "ls %s" % parser["SlaveOS_mount_nfs_folder"]
    
    t_start = time.time()
    
    while (time.time() - t_start) < parser["pre_node_wait_mount_nfs_time"]:
        time.sleep(1)
        s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
        if s_stdout != "":
            return True
    return False
    
def preprocess(parser):
  """
  when test case start, preprocess something

  :param parser: is a dict, get from Test config file
  """
  preprocess_mm(parser)
  print "pre"
  preprocess_hostOS(parser)
  print "pre1"
  preprocess_backupOS(parser)

def preprocess_mm(parser):
  """
  preprocess master monitor part

  :called func: preprocess
  :param parser: is a dict, get from Test config file
  """
  if parser["pre_check_mm"] == "yes": #若需確認master monitor之狀態，則進入
    if master_monitor.get_status() != "running":
      #master_monitor.temp_start()
      time.sleep(float(parser["pre_mm_start_time"]))
      if master_monitor.get_status() != "running":
        raise TA_error.Preprocess_Error("master monitor can not start")

  if parser["pre_init_mm"] == "yes":
    #print 99
    cmd = "bash initAll.sh"
    status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
    #print status
    #print 100

def preprocess_hostOS(parser):
  """
  preprocess HostOS

  :called func: preprocess
  :param parser: is a dict, get from Test config file
  """
  #preprocess_hostOS_hw(parser)
  """
  because of some unknow problem of FTKVM , we can't check HostOS status 
  """
  #preprocess_hostOS_OS(parser)
  
  #preprocess_hostOS_wd(parser)
  print 46
  preprocess_hostOS_FTsystem(parser)
  print 47
  preprocess_hostOS_vm(parser)
  print 48


def preprocess_backupOS(parser):
  """
  preprocess backupOS

  :called func: preprocess
  :param parser: is a dict, get from Test config file
  """
  #preprocess_backupOS_OS(parser)
  #preprocess_backupOS_FTsystem(parser)
  #print 9
  preprocess_backupOS_vm(parser)
  #print 10

def preprocess_hostOS_hw(parser):
  """
  perprocess hostOS hardware part

  :called func: preprocess_hostOS
  :param parser: is a dict, get from Test config file
  """
  if parser["pre_check_hostOS_hw"] == "yes":
    if mmsh.stateshmgr(parser["HostOS_shmgr_name"]) == "stop":
      raise TA_error.Preprocess_Error("HostOS hw shmgr stop")
    if mmsh.stateipmc(parser["HostOS_ipmc_name"]) == "stop":
      raise TA_error.Preprocess_Error("HostOS hw ipmc stop")

def preprocess_hostOS_OS(parser):
  """
  preprocess hostOS OS part

  :called func: preprocess_hostOS
  :param parser: is a dict, get from Test config file 
  """
  if parser["pre_check_FT_hostOS"] == "yes":
    if parser["pre_FT_hostOS_status"] == "running":
      preprocess_hostOS_OS_boot(parser)
    elif parser["pre_FT_hostOS_status"] == "shutdown":
      preprocess_hostOS_OS_shutdown(parser)

def preprocess_hostOS_OS_boot(parser):
  """
  preprocess hostOS OS boot part

  :called func: preprocess_hostOS_OS
  :param parser: is a dict, get from Test config file
  """
  if not FTOS.is_running(parser["HostOS_name"]):
    if FTOS.is_shutdown(parser["HostOS_name"]):
      status = FTOS.boot(parser["HostOS_name"])
      if status != "success":
        raise TA_error.Preprocess_Error("HostOS OS boot command fail")
    time.sleep(float(parser["pre_hostOS_boot_time"]))
    if not FTOS.is_running(parser["HostOS_name"]):
      raise TA_error.Preprocess_Error("HostOS OS can not boot")
  

def preprocess_hostOS_OS_shutdown(parser):
  """
  preprocess hostOS OS shutdown part

  :called func: preprocess_hostOS_OS
  :param parser: is a dict, get from Test config file
  """
  if not FTOS.is_shutdown(parser["HostOS_name"]): #若host不為關機狀態
    if FTOS.is_running(parser["HostOS_name"]):
      status = FTOS.shutdown(parser["HostOS_name"])
      if status != "success":
        raise TA_error.Preprocess_Error("HostOS OS shutdown command fail")
    time.sleep(float(parser["pre_hostOS_shutdown_time"]))
    if not FTOS.is_shutdown(parser["HostOS_name"]):
      raise TA_error.Preprocess_Error("HostOS OS can not shutdown")

def preprocess_backupOS_OS(parser):
  """
  preprocess backupOS OS part

  :called func: preprocess_backupOS_OS
  :param parser: is a dict, get from Test config file
  """
  if parser["pre_check_FT_hostOS"] == "yes":
    if parser["pre_FT_hostOS_status"] == "running":
      preprocess_hostOS_OS_boot(parser)
    elif parser["pre_FT_hostOS_status"] == "shutdown":
      pass

def preprocess_backupOS_OS_boot(parser):
  """
  preprocess backupOS OS boot

  :called func: preprocess_hostOS_OS
  :param parser: is a dict, get from Test config file
  """
  if not FTOS.is_running(parser["BackupOS_name"]):
    if FTOS.is_shutdown(parser["BackupOS_name"]):
      status = FTOS.boot(parser["BackupOS_name"])
      if status != "success":
        raise TA_error.Preprocess_Error("BackupOS OS boot command fail")
    time.sleep(float(parser["pre_backupOS_boot_time"]))
    if not FTOS.is_running(parser["BackupOS_name"]):
      raise TA_error.Preprocess_Error("BackupOS OS can not boot")

def preprocess_hostOS_wd(parser):
  """
  preprocess watchdog for fault tolerant hardware part

  :called func: preprocess_hostOS
  :param parser: is a dict, get from Test config file
  """
  if parser["pre_check_hostOS_hw"] == "yes":
    if mmsh.statewd(parser["HostOS_name"]) == "stop":
      status = mmsh.startwd(parser["HostOS_name"])
      if status != "success":
        raise TA_error.Preprocess_Error("HostOS watchdog process can not start")
  

def preprocess_hostOS_FTsystem(parser):
  """
  preprocess HostOS FTsystem part
  
  check FTsystem status 

  start/stop FTsystem

  raise exception if FTsystem can not start/stop

  :called func: preprocess_hostOS
  :param parser: is a dict, get from Test config file
  """
  if parser["pre_check_hostOS_FTsystem"] == "yes":
    ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
    status = FTsystem.get_status(ssh)
    if status == "not running" and parser["pre_hostOS_FTsystem_start"] == "yes": #若狀態不為running且根據參數必需是running則進入
        FTsystem.start(ssh) #透過ssh開啟libvirt
        time.sleep(float(parser["pre_hostOS_FTsystem_start_time"]))
        if FTsystem.get_status(ssh) == "not running": #若狀態不為running則raise exception
            ssh.close()
        raise TA_error.Preprocess_Error("HostOS FTsystem can not start")
    if status == "running" and parser["pre_hostOS_FTsystem_start"] == "no": #若狀態為running且根據參數必需不是running則進入
        FTsystem.stop(ssh)
        time.sleep(float(parser["pre_hostOS_FTsystem_start_time"]))
        if FTsystem.get_status(ssh) == "running": #若狀態為running則raise exception
            ssh.close()
        raise TA_error.Preprocess_Error("HostOS FTsystem can not stop")
    ssh.close()


def preprocess_backupOS_FTsystem(parser):
  """
  preprocess backupOS FTsystem part
  
  check FTsystem status 

  start/stop FTsystem

  raise exception if FTsystem can not start/stop

  :called func: preprocess_backupOS_OS
  :param parser: is a dict, get from Test config file
  """
  if parser["pre_check_backupOS_FTsystem"] == "yes":
    ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
    status = FTsystem.get_status(ssh)
    if status == "not running" and parser["pre_backupOS_FTsystem_start"] == "yes": #若狀態不為running且根據參數必需是running則進入
      FTsystem.start(ssh) #透過ssh開啟libvirt
      time.sleep(float(parser["pre_backupOS_FTsystem_start_time"]))
      if FTsystem.get_status(ssh) == "not running": #若狀態不為running則raise exception
        ssh.close()
        raise TA_error.Preprocess_Error("backupOS FTsystem can not start")
    if status == "running" and parser["pre_backupOS_FTsystem_start"] == "no": #若狀態為running且根據參數必需不是running則進入
      FTsystem.stop(ssh)
      time.sleep(float(parser["pre_backupOS_FTsystem_start_time"]))
      if FTsystem.get_status(ssh) == "running": #若狀態為running則raise exception
        ssh.close()
        raise TA_error.Preprocess_Error("backupOS FTsystem can not stop")
    ssh.close()
  

def preprocess_hostOS_vm(parser):
  """
  preprocess hostOS vm part

  :called func: preprocess_hostOS
  :param parser: is a dict, get from Test config file
  """
  if parser["pre_check_hostOS_VM"] == "yes":
    if parser["pre_hostOS_VM_status"] == "running":
      print 51
      preprocess_hostOS_vm_running(parser)
      if parser["pre_hostOS_VM_login"] == "yes":
        print 52
        preprocess_hostOS_vm_login(parser)
        print 53
    elif parser["pre_hostOS_VM_status"] == "shut off":
      preprocess_hostOS_vm_shutdown(parser)
    elif parser["pre_hostOS_VM_status"] == "paused":
      pass


def preprocess_hostOS_vm_running(parser):
  """
  preprocess vm become running

  :called func: preprocess_hostOS_vm
  :param parser: is a dict, get from Test config file
  """
  ssh = shell_server.get_ssh(parser["HostOS_ip"]
                            , parser["HostOS_usr"]
                            , parser["HostOS_pwd"]) #獲得ssh

  if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"], ssh):
    print 59
    if "pre_hostOS_VM_restart" in parser.keys() and parser["pre_hostOS_VM_restart"] == "yes": #根據參數若VM需重新啟動
      print 54
      prepocess_hostOS_vm_restart(parser)
      print 55
      time.sleep(float(parser["pre_hostOS_VM_boot_time"]))
  elif FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"], ssh):
    print 56
    prepocess_hostOS_vm_start(parser)
    print 57
    time.sleep(float(parser["pre_hostOS_VM_boot_time"]))
  print 58
  if not FTVM.is_running(parser["vm_name"], parser["HostOS_ip"], ssh):
    ssh.close()
    raise TA_error.Preprocess_Error("HostOS VM: %s can not start" % parser["vm_name"])

  ssh.close()

def prepocess_hostOS_vm_start(parser):
  """
  according to fault tolerant level, preprocess vm start

  :called func: preprocess_hostOS_vm_running
  :param parser: is a dict, get from Test config file
  """
  ssh = shell_server.get_ssh(parser["HostOS_ip"]
                        , parser["HostOS_usr"]
                        , parser["HostOS_pwd"]) #獲得ssh

  if parser["level"] == "0": #若為不開啟容錯機制之開機，則進入
    #print 58
    FTVM.start(parser["vm_name"], parser["HostOS_ip"], ssh)
    #print 58.5
  else:
    #print parser["level"]
    FTVM.ftstart(parser["vm_name"], parser["HostOS_ip"], parser["level"], ssh)
    #print 59
  ssh.close()

def prepocess_hostOS_vm_restart(parser):
  """
  according to fault tolerant level, preprocess vm restart

  :called func: preprocess_hostOS_vm_running
  :param parser: is a dict, get from Test config file
  """
  ssh = shell_server.get_ssh(parser["HostOS_ip"]
                        , parser["HostOS_usr"]
                        , parser["HostOS_pwd"]) #獲得ssh

  if parser["level"] == "0": #若為不開啟容錯機制之重新啟動，則進入
    FTVM.restart(parser["vm_name"], parser["HostOS_ip"],ssh)
  else:
    FTVM.ftrestart(parser["vm_name"], parser["HostOS_ip"], parser["level"], ssh)

def preprocess_hostOS_vm_shutdown(parser):
  """
  preprocess hostOS vm become shutdown

  :called func: preprocess_hostOS_vm
  :param parser: is a dict, get from Test config file
  """

  ssh = shell_server.get_ssh(parser["HostOS_ip"]
                        , parser["HostOS_usr"]
                        , parser["HostOS_pwd"]) #獲得ssh
  if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"], ssh):
    FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"], ssh)
    time.sleep(float(parser["pre_hostOS_VM_shutdown_time"]))
  elif FTVM.is_paused(parser["vm_name"], parser["HostOS_ip"], ssh):
    FTVM.resume(parser["vm_name"], parser["HostOS_ip"], ssh)
    FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"], ssh)
    time.sleep(float(parser["pre_hostOS_VM_shutdown_time"]))
  if not FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"], ssh):
    ssh.close()
    raise TA_error.Preprocess_Error("HostOS %s can not shutdown" % parser["vm_name"])
  ssh.close()

def preprocess_hostOS_vm_login(parser):
  """
  preprocess check hostOS vm is login

  :called func: preprocess_hostOS_OS_vm
  :param parser: is a dict, get from Test config file
  """
  if not FTVM.is_login(parser["vm_name"]
                  , parser["TA_ip"]
                  , parser["TA_msg_sock_port"]
                  , int(parser["pre_hostOS_VM_login_time"])):
    raise TA_error.Preprocess_Error("HostOS %s is not login" % parser["vm_name"])

def preprocess_backupOS_vm(parser):
  """
  preprocess backupOS vm

  :called func: preprocess_backupOS
  :param parser: is a dict, get from Test config file
  """
  if parser["pre_check_backupOS_VM"] == "yes":
    if parser["pre_backupOS_VM_status"] == "running":
      preprocess_backupOS_vm_running(parser)
    elif parser["pre_backupOS_VM_status"] == "shut off":
      preprocess_backupOS_vm_shutdown(parser)
    elif parser["pre_backupOS_VM_status"] == "paused":
      pass

def preprocess_backupOS_vm_shutdown(parser):
  """
  preprocess backupOS vm become shutdown

  :called func: preprocess_backupOS_vm
  :param parser: is a dict, get from Test config file
  """
  print "GG"
  ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                            , parser["BackupOS_usr"]
                            , parser["BackupOS_pwd"]) #獲得ssh
  if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"],ssh):
    FTVM.shutdown(parser["vm_name"], parser["BackupOS_ip"],ssh)
    time.sleep(float(parser["pre_backupOS_VM_shutdown_time"]))
  elif FTVM.is_paused(parser["vm_name"], parser["BackupOS_ip"],ssh):
    FTVM.resume(parser["vm_name"], parser["BackupOS_ip"],ssh)
    FTVM.shutdown(parser["vm_name"], parser["BackupOS_ip"],ssh)
    time.sleep(float(parser["pre_backupOS_VM_shutdown_time"]))
  if not FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"],ssh):
    ssh.close()
    raise TA_error.Preprocess_Error("backupOS %s can not shutdown" % parser["vm_name"])
  ssh.close()

def preprocess_backupOS_vm_running(parser):
  """
  according to fault tolerant level, preprocess vm start

  :called func: preprocess_hostOS_vm_running
  :param parser: is a dict, get from Test config file
  """
  ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                          , parser["BackupOS_usr"]
                          , parser["BackupOS_pwd"]) #獲得ssh
  if parser["level"] == "0": #若為不開啟容錯機制之開機，則進入
    FTVM.start(parser["vm_name"], parser["BackupOS_ip"], ssh)
  else:
    FTVM.ftstart(parser["vm_name"], parser["BackupOS_ip"], parser["level"], ssh)
  ssh.close()

if __name__ == '__main__':
  ssh = paramiko.SSHClient()
  ssh.load_system_host_keys()
  ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  ssh.connect("140.115.53.42", username="ting", password="oolabting")
  #s_stdin, s_stdout, s_stderr = ssh.exec_command("service libvirt-bin status | egrep -oi '([0-9]+)$'")
  #print "output", s_stdout.read()
  s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo service libvirt-bin start")
  #print s_stdout.readlines()
  ssh.close()