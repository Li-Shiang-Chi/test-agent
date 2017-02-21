#/usr/bin/python
#-*- coding: utf-8 -*-
import paramiko
import time
import subprocess
import shell_server
import FTVM
import FTsystem
import master_monitor
import mmsh
import TA_error
import HAagent_info
import HAagent
import HAagent_terminal

def backupOS_role_is_Slave_on_MasterOS(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                      , parser["HostOS_usr"]
                      , parser["HostOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["BackupOS_name"], ssh)
	ssh.close()
	if role == "slave": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not slave" % parser["HostOS_name"])

def hostOS_role_is_Slave_on_BackupOS(parser):
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                      , parser["BackupOS_usr"]
                      , parser["BackupOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["HostOS_name"], ssh)
	ssh.close()
	if role == "slave": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not slave" % parser["HostOS_name"])

def backupOS_role_is_Master_on_BackupOS(parser):

	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                      , parser["BackupOS_usr"]
                      , parser["BackupOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["BackupOS_name"], ssh)
	ssh.close()
	if role == "master": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not slave" % parser["HostOS_name"])

def hostOS_role_is_Master(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                      , parser["HostOS_usr"]
                      , parser["HostOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["HostOS_name"], ssh)
	ssh.close()
	if role == "master": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not master" % parser["HostOS_name"])

def hostOS_role_is_Backup(parser):
	role = mmsh.inforole(parser["HostOS_name"])
	if role == "backup": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not backup" % parser["HostOS_name"] )

def hostOS_role_is_Slave(parser):
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                      , parser["BackupOS_usr"]
                      , parser["BackupOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["HostOS_name"], ssh)
	if role == "slave": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not slave" % parser["HostOS_name"])

def backupOS_role_is_Master(parser):
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                      , parser["BackupOS_usr"]
                      , parser["BackupOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["BackupOS_name"], ssh)
	if role == "master": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not master" % parser["BackupOS_name"])

def backupOS_role_is_Backup(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                      , parser["HostOS_usr"]
                      , parser["HostOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["BackupOS_name"],ssh)
	if role == "backup": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not backup." % parser["BackupOS_name"])

def backupOS_role_is_Slave(parser):

	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                      , parser["BackupOS_usr"]
                      , parser["BackupOS_pwd"]) #獲得ssh

	role = mmsh.inforole(parser["BackupOS_name"], ssh)
	ssh.close()
	if role == "slave": 
		return True
	raise TA_error.Assert_Error("Host (name : %s) role is not slave." % parser["BackupOS_name"])


def detect_hostOS_crash(parser):
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                          , parser["BackupOS_usr"]
                          , parser["BackupOS_pwd"]) #獲得ssh

	if mmsh.statehost(parser["HostOS_name"], ssh) == "shutdown": #若回傳之狀態是hardware shutdown，則test oracle通過，否則raise exception
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("Host (name : %s) has not detect host os crash " % parser["HostOS_name"])

def detect_BackupOS_crash(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                          , parser["HostOS_usr"]
                          , parser["HostOS_pwd"]) #獲得ssh

	if mmsh.statehost(parser["BackupOS_name"], ssh) == "shutdown": #若回傳之狀態是hardware shutdown，則test oracle通過，否則raise exception
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("Host (name : %s) has not detect host os crash " % parser["BackupOS_name"])

def hostOS_status_is_M4(parser):
	"""
	host hardware status is M4 or not

	M4 means hardware ok
	:param parser: config 
	:return: True/raise: exception
	"""
	if "ast_hostOS_running_wait_time" in parser.keys(): #若參數ast_hostOS_running_wait_time存在於parser，則進入
		time.sleep(int(parser["ast_hostOS_running_wait_time"]))
	#print mmsh.stateipmc(parser["HostOS_name"])
	if mmsh.stateipmc(parser["HostOS_name"]) == "M4": #若回傳之狀態是M4，則該test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("Host (name : %s) hardware status is not M4" % parser["HostOS_name"])

#---
def hostOS_status_is_running(parser):
	"""
	hostOS status is running or not
	:param parser: config 
	:return: True/raise exception
	"""
	if "ast_hostOS_running_wait_time" in parser.keys(): #若參數ast_hostOS_running_wait_time存在於parser，則進入
		time.sleep(int(parser["ast_hostOS_running_wait_time"]))
	#print mmsh.statehost(parser["HostOS_name"])
	if mmsh.statehost(parser["HostOS_name"]) == "running": #若回傳之狀態是running，則test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("Host (name : %s) status is not running" % parser["HostOS_name"])


def vm_running_in_hostOS(parser):
	"""
	vm is running in hostOS or not

	:param parser: config
	:return: True/raise exception
	"""

	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                  , parser["HostOS_usr"]
                  , parser["HostOS_pwd"]) #獲得ssh

	t_end = time.time()
	if "ast_vm_running_wait_time" in parser.keys(): #若參數ast_vm_running_wait_time存在於parser，則進入
		t_end = time.time()+float(parser["ast_vm_running_wait_time"]) #計算出等待之時間，並存於t_end
	while time.time() < t_end: #超過t_end則跳出迴圈
		#每sleep一秒就詢問一次狀態
		time.sleep(1)
		if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"], ssh): #狀態為running就跳出迴圈
			break
	if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"], ssh): #若回傳之狀態是running，則test oracle通過，否則raise exception
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) is not running in hostOS" % parser["vm_name"])

def vm_shudown_in_hostOS(parser):
	"""
	vm is running in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                  , parser["HostOS_usr"]
                  , parser["HostOS_pwd"]) #獲得ssh
	if FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"],ssh): #若回傳之狀態是shut off，則test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("VM (name : %s) is not shutdown in hostOS" % parser["vm_name"])

def vm_is_login_in_hostOS(parser):
	"""
	vm is login in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	
	print 577
	if FTVM.is_login(parser["vm_name"]
				  , parser["TA_ip"]
				  , parser["TA_msg_sock_port"]
				  , int(parser["ast_vm_login_wait_time"])): #若回傳VM登入完成，則test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("VM (name : %s) is not login in hostOS" % parser["vm_name"])
	
		

def vm_is_login_in_backupOS(parser):
	"""
	vm is login in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	

	if FTVM.is_login(parser["vm_name"]
				  , parser["TA_ip"]
				  , parser["TA_msg_sock_port"]
				  , int(parser["ast_vm_login_wait_time"])): #若回傳VM登入完成，則test oracle通過，否則raise exception
		return True
	raise TA_error.Assert_Error("VM (name : %s) is not login in backupOS" % parser["vm_name"])	


def vm_running_in_backupOS(parser):
	"""
	vm is running in backupOS or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                  , parser["BackupOS_usr"]
                  , parser["BackupOS_pwd"]) #獲得ssh

	print 64
	t_end = time.time()
	if "ast_vm_running_wait_time" in parser.keys(): #若參數ast_vm_running_wait_time存在於parser，則進入
		t_end = time.time()+float(parser["ast_vm_running_wait_time"]) #計算出等待之時間，並存於t_end
	print 65
	while time.time() < t_end: #超過t_end則跳出迴圈
		#每sleep一秒就詢問一次狀態
		time.sleep(1)
		print 66
		if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh): #狀態為running就跳出迴圈
			break
	print 67
	if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh): #若回傳之狀態是running，則test oracle通過，否則raise exception
		ssh.close()
		return True
	print 68
	ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) is not running in backupOS" % parser["vm_name"])


def FTsystem_running_in_hostOS(parser):
	"""
	FTsystem is running in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲取ssh

	if FTsystem.get_status(ssh) == "running": #透過ssh詢問FTsystem之狀態是否為running
		ssh.close()
		return True

	ssh.close()
	raise TA_error.Assert_Error("FTsystem is not running in hostOS")

def detect_fail(parser):
	"""
	FTsystem find fail or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲取ssh
	if mmsh.infofail(parser["vm_name"],ssh) != "no fail":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no fail in hostOS" % parser["vm_name"])

def detect_no_fail(parser):
	"""
	FTsystem find no fail or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲取ssh	
	if mmsh.infofail(parser["vm_name"],ssh) == "no fail":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has fail in hostOS" % parser["vm_name"])

def detect_fail_vm_crash(parser):
	"""
	FTsystem find fail and fail is vm crash or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲取ssh
	print 558
	if "ast_vm_crash_time" in parser.keys(): #若參數ast_vm_crash_time存在於parser，則進入
		time.sleep(int(parser["ast_vm_crash_time"]))
	if mmsh.infofail(parser["vm_name"] ,ssh) == "vm crash":
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("VM (name : %s) has not detect vm crash in hostOS" % parser["vm_name"])

def detect_fail_os_crash(parser):
	"""
	FTsystem find fail and fail is os crash or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲取ssh

	if mmsh.infofail(parser["vm_name"],ssh) == "vm os crash":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has not detect vm os crash" % parser["vm_name"])

def do_recovery(parser):
	"""
	FTsystem do recovery or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲取ssh

	if mmsh.inforecover(parser["vm_name"],ssh) != "no recover":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no recovery" % parser["vm_name"])


def no_recovery(parser):
	"""
	FTsystem no recover or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲取ssh

	if mmsh.inforecover(parser["vm_name"],ssh) == "no recover":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has recovery" % parser["vm_name"])

def recovery_vm_p_restart(parser):
	"""
	FTsystem recover vm process restart or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲取ssh

	if "ast_vm_p_restart_time" in parser.keys(): #若參數ast_vm_p_restart_time存在於parser，則進入
		time.sleep(int(parser["ast_vm_p_restart_time"]))
	if mmsh.inforecover(parser["vm_name"], ssh) == "vm process restart":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no recovery : vm process restart" % parser["vm_name"])

def recovery_vm_reboot(parser):
	"""
	FTsystem recover vm reboot or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲取ssh

	if mmsh.inforecover(parser["vm_name"],ssh) == "vm reboot":
		return True
	raise TA_error.Assert_Error("VM (name : %s) has no recovery : vm reboot" % parser["vm_name"])

def libvirt_running_in_hostOS(parser):
	"""
	libvirt process is running in hostOS or not
	:param parser: config
	:return: True/raise exception
	"""
	if "ast_libvirt_running_wait_time" in parser.keys(): #若參數ast_libvirt_running_wait_time存在於parser，則進入
		 time.sleep(float(parser["ast_libvirt_running_wait_time"]))
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	if FTsystem.is_running(ssh):
		return True
	ssh.close()
	raise TA_error.Assert_Error("libivrt isn't running")

def master_monitor_running(parser):
	"""
	master monitor running or not
	:param parser: config
	:return: True/raise exception
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                      , parser["BackupOS_usr"]
                      , parser["BackupOS_pwd"]) #獲得ssh

	if "ast_mm_running_wait_time" in parser.keys(): #若參數ast_mm_running_wait_time存在於parser，則進入
		 time.sleep(float(parser["ast_mm_running_wait_time"]))
	if master_monitor.is_running(ssh):
		ssh.close()
		return True
	ssh.close()
	raise TA_error.Assert_Error("master_monitor isn't running")

def test(parser):
	"""
	test when raise exception
	"""
	raise TA_error.Assert_Error("test FTVMTA log feature")

	"""
	cluster created or not
	:param parser: config
	:return: True/raise exception
	"""
def detect_create_cluster(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	cluster = "test_c"
	success =  HAagent_info.is_cluster_exist(cluster, parser)
	ssh.close()	
	
	if success :
		return True
	raise TA_error.Assert_Error("create cluster fail")
	"""
	duplicate cluster created or not
	:param parser: config
	:return: True/raise exception
	"""
def detect_create_duplicate_cluster(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	out = HAagent.create_cluster("test_c", "test_n", "127.0.0.1", "9999", parser, ssh)
	success = (HAagent_terminal.Already_in_cluster in out)
	ssh.close()

	if success :
		return True
	raise TA_error.Assert_Error("create duplicate cluster fail")
	
	"""
	cluster deleted or not
	:param parser: config
	:return: True/raise exception
	"""
def detect_de_cluster(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	cluster = "test_c"
	
	success = HAagent_info.is_cluster_exist(cluster, parser)
	ssh.close()
	
	if not success:
		return True
	raise TA_error.Assert_Error("de cluster fail")

	"""
	non-primary node (in this test case is backup node) delete cluster or not
	:param parser: config
	:return: True/raise exception
	"""


def detect_non_primary_de_cluster(parser):
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
	
	
	cluster = "test_c"
	
	success = HAagent_info.is_cluster_exist(cluster, parser)
	
	if success:
		return True
	raise TA_error.Assert_Error("non primary de cluster fail")
	
	"""
	outer cluster deleted or not
	:param parser: config
	:return: True/raise exception
	"""
def detect_de_outer_cluster(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	cluster = "test_b"
	success = HAagent_info.is_cluster_exist(cluster, parser)
	ssh.close()	
	
	if success:
		return True
	raise TA_error.Assert_Error("de outer cluster fail")

	"""
	detect add node to cluster or not
	:param parser: config
	:return: True/raise exception
	"""

def detect_add_node(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh

	primary_success = HAagent_info.is_add_primary_success(parser)
	backup_success = HAagent_info.is_add_backup_success(parser)
	#slave_success = HAagent_info.is_add_slave_success(parser)
	
	ssh.close()
	
	if not primary_success:
		raise TA_error.Assert_Error("primary add node fail")
	if not backup_success:
		raise TA_error.Assert_Error("backup add node fail")
	#if not slave_success:
	#	raise TA_error.Assert_Error("slave add node fail")
	return True
	
	"""
	detect add duplicate node to cluster or not
	:param parser: config
	:return: True/raise exception
	"""

def detect_add_duplicate_node(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	out = HAagent.add_node(parser["Cluster_name"], parser["HostOS_name"], parser["HostOS_ip"] , parser["HostOS_ipmb"], parser, ssh)
	print out
	success = (HAagent_terminal.Node_name_repeat in out)
	ssh.close()

	if success:
		return True
	raise TA_error.Assert_Error("add duplicate node fail")
	"""
	detect add outer node to cluster or not
	:param parser: config
	:return: True/raise exception
	"""

def detect_add_outer_node(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	out = HAagent.add_node("test_b", "test_n", "127.0.0.1", "9999", parser, ssh)
	success = (HAagent_terminal.Not_in_cluster in out)
	ssh.close()

	if success:
		return True
	raise TA_error.Assert_Error("add node fail")

	"""
	detect use non-primary node add node success or not
	:param parser: config
	:return: True/raise exception
	"""
def detect_non_primary_node_add_node(parser):
	
	success = HAagent_info.is_node_exists(parser["Cluster_name"], parser["SlaveOS_name"], parser)
	
	if not success:
		return True
	raise TA_error.Assert_Error("non primary node add node fail")
	

	"""
	detect remove node or not
	:param parser: config
	:return: True/raise exception
	"""
def detect_de_node(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	success = HAagent_info.is_node_exists("test_c", "test_n", parser)
	
	
	ssh.close()
	if success:
		raise TA_error.Assert_Error("de node fail")
	return True

	"""
	detect remove node or not
	:param parser: config
	:return: True/raise exception
	"""
def detect_non_primary_de_node(parser):
	success = HAagent_info.is_node_exists(parser["Cluster_name"], parser["HostOS_name"], parser)
	
	if success:
		return True
	raise TA_error.Assert_Error("non primary de node fail")



	"""
	detect overview function is ok or not
	:param parser: config
	:return: True/raise exception
	"""

def detect_overview(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	out = HAagent.overview(parser, ssh)	
	success = (HAagent_terminal.overview in out)
	
	if success:
		return True
	raise TA_error.Assert_Error("overview fail")

if __name__ == '__main__':
	parser = {}
	parser["BackupOS_ip"] = "140.115.53.132"
	parser["BackupOS_usr"] = "user"
	parser["BackupOS_pwd"] = "000000"
	parser["HostOS_name"] = "h2"
	parser["BackupOS_name"] = "h2"
	
	print backupOS_role_is_Master_on_BackupOS(parser)

	
