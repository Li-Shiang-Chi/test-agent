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
import TA_error
import mmsh
import HAagent
import NFS


def run_postprocess(parser):
	"""
	when test done , each node will do postprocess
	:param parser: is a dict, get from Test config file
	""" 
	postprocess_Host(parser)
	postprocess_Backup(parser)
	postprocess_NFS(parser)
    
def postprocess_Host(parser):
	"""
	when test done , primary postprocess
	:param parser: is a dict, get from Test config file
	""" 
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh 
	
	postProcessHostOSReboot(parser)
	ssh.close()
    
def postprocess_Backup(parser):
	"""
	when test done , Backup postprocess
	:param parser: is a dict, get from Test config file
	""" 
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh 
	postProcessBackupOSReboot(parser)
	ssh.close()
    
def postprocess_Slave(parser):
	"""
	when test done , Slave postprocess
	:param parser: is a dict, get from Test config file
	""" 
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh 
	postProcessSlaveOSReboot(parser)
	ssh.close()
 
    
def postprocess_NFS(parser):
	"""
	when test done , NFS postprocess
	:param parser: is a dict, get from Test config file
	""" 
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	postprocessResetNFS(parser, ssh)
	
	
def postProcessHostOSReboot(parser):
	"""
	when test case done , Host OS reboot
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh 
	
	cmd = "reboot"
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close(); 
	
def postProcessBackupOSReboot(parser):
	"""
	when test case done , Host OS reboot
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh 
	
	cmd = "reboot"
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close(); 
	
def postProcessSlaveOSReboot(parser):
	"""
	when test case done , Host OS reboot
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["SlaveOS_ip"]
                              , parser["SlaveOS_usr"]
                              , parser["SlaveOS_pwd"]) #獲得ssh 
	
	cmd = "reboot"
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close();
def postProcessNFSOSReboot(parser):
	"""
	when test case done , Host OS reboot
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["nfs_ip"]
                              , parser["nfs_usr"]
                              , parser["nfs_pwd"]) #獲得ssh 
	
	cmd = "reboot"
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close(); 	
     
def postprocessResetNFS(parser,ssh):
	"""
	when test done , clear nfs file

	:param parser: is a dict, get from Test config file
	:param ssh : shell server
	""" 
	NFS.reset(parser, ssh)
	
def postprocess(parser):
	"""
	when testing done, postprocess something

	:param parser: is a dict, get from Test config file
	"""
	time.sleep(1)
	print "POST"
	postprocess_hostOS(parser)
	print "POST1"
	postprocess_backupOS(parser)

def postprocess_hostOS(parser):
	"""
	postprocess hostOS

	:called func: postprocess
	:param parser: is a dict, get from Test config file
	"""
	#postprocess_hostOS_OS(parser)
	postprocess_hostOS_FTsystem(parser)
	print "POST2"
	postprocess_hostOS_vm(parser)
	print "POST3"
	postprocess_hostOS_OS_running(parser)
	
def postprocess_backupOS(parser):
	"""
	postprocess backupOS

	:called func: postprocess
	:param parser: is a dict, get from Test config file
	"""
	postprocess_backupOS_vm(parser)
	print "POST4"
	postprocess_backupOS_OS_running(parser)
	print "POST5"
	postprocess_hostOS_ATCA_OS_running(parser)
	print "POST6"
	postprocess_backupOS_ATCA_OS_running(parser)

def postprocess_hostOS_OS(parser):
	"""
	postprocess hostOS OS part

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_hostOS_shutdown"] == "yes": #若pos_hostOS_shutdown為yes則進入
		if mmsh.statehost(parser["HostOS_name"]) != "shutdown": #詢問mmsh，vm所在host的狀態，若不為shutdown 則進行關機之動作
			mmsh.stophost(parser["HostOS_name"])
			time.sleep(float(parser["pos_hostOS_shutdown_time"]))
	if mmsh.statehost(parser["HostOS_name"]) != "shutdown": #若狀態不為shutdown則raise exception
		raise TA_error.Postprocess_Error("HostOS can not shutdown")


def postprocess_hostOS_FTsystem(parser):
	"""
	postprocess HostOS FTsystem part

	check FTsystem status 

	start/stop FTsystem

	raise exception if FTsystem can not start/stop

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_hostOS_FTsystem"] == "yes":
		ssh = shell_server.get_ssh(parser["HostOS_ip"]
								, parser["HostOS_usr"]
								, parser["HostOS_pwd"]) #獲得ssh
		status = FTsystem.get_status(ssh) #獲得libvirt status
		if status == "not running" and parser["pos_hostOS_FTsystem_start"] == "yes": #若狀態不為running且根據參數pos_hostOS_FTsystem_start必須為running，則進入
			FTsystem.start(ssh) #透過ssh開啟libvirt
			time.sleep(float(parser["pos_hostOS_FTsystem_start_time"]))
			if FTsystem.get_status(ssh) == "not running": #若狀態不為running則raise exception
				ssh.close()
				raise TA_error.Postprocess_Error("HostOS FTsystem can not start")
		if status == "running" and parser["pos_hostOS_FTsystem_start"] == "no": #若狀態為running且根據參數pos_hostOS_FTsystem_start必須不為running，則進入
			FTsystem.stop(ssh) #透過ssh關閉libvirt
			time.sleep(float(parser["pos_hostOS_FTsystem_start_time"]))
			if FTsystem.get_status(ssh) == "running": #若狀態為running則raise exception
				ssh.close()
				raise TA_error.Postprocess_Error("HostOS FTsystem can not stop")
		ssh.close()


def postprocess_hostOS_vm(parser):
	"""
	postprocess hostOS vm part

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_hostOS_VM"] == "yes": #需要確認VM狀態，則進入
		if parser["pos_hostOS_VM_status"] == "running":
			postprocess_hostOS_vm_running(parser)
		elif parser["pos_hostOS_VM_status"] == "shut off":
			postprocess_hostOS_vm_shutdown(parser)
		elif parser["pos_hostOS_VM_status"] == "paused":
			pass

def postprocess_hostOS_vm_running(parser):
	"""
	postrocess vm become running

	:called func: postprocess_hostOS_vm
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
							, parser["HostOS_usr"]
							, parser["HostOS_pwd"]) #獲得ssh
	if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"], ssh):
		FTVM.restart(parser["vm_name"], parser["HostOS_ip"], ssh)
	elif FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"], ssh):
		FTVM.start(parser["vm_name"], parser["HostOS_ip"], ssh)
	time.sleep(float(parser["pos_hostOS_VM_boot_time"]))
	if not FTVM.is_running(parser["vm_name"], parser["HostOS_ip"], ssh):
		ssh.close()
		raise TA_error.Postprocess_Error("HostOS %s can not start" % parser["vm_name"])
	ssh.close()

def postprocess_hostOS_vm_shutdown(parser):
	"""
	postprocess vm become shutdown

	:called func: postprocess_hostOS_vm
	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
							, parser["HostOS_usr"]
							, parser["HostOS_pwd"]) #獲得ssh

	if FTVM.is_running(parser["vm_name"], parser["HostOS_ip"], ssh):
		print "shutdown now 1"
		time.sleep(float(parser["post_hostOS_wait_VM_enable_shutdown_time"]))
		FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"], ssh)
	elif FTVM.is_paused(parser["vm_name"], parser["HostOS_ip"], ssh):
		print "shutdown now 2"
		time.sleep(float(parser["post_hostOS_wait_VM_enable_shutdown_time"]))
		FTVM.resume(parser["vm_name"], parser["HostOS_ip"], ssh)
		FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"], ssh)
	time.sleep(float(parser["pos_hostOS_VM_shutdown_time"]))
	#print FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"])

	if not FTVM.is_shutoff(parser["vm_name"], parser["HostOS_ip"], ssh):
		ssh.close()
		raise TA_error.Postprocess_Error("HostOS %s can not shutdown" % parser["vm_name"])

	ssh.close()

def postprocess_backupOS_vm(parser):
	"""
	postprocess backupOS vm part

	:called func: postprocess_backupOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_backupOS_VM"] == "yes":
		if parser["pos_backupOS_VM_status"] == "running":
			#postprocess_backupOS_vm_running(parser)
			pass
		elif parser["pos_backupOS_VM_status"] == "shut off":
			postprocess_backupOS_vm_shutdown(parser)
		elif parser["pos_backupOS_VM_status"] == "paused":
			pass

def postprocess_backupOS_vm_shutdown(parser):
	"""
	postprocess backupOS vm shutdown

	:called func: postprocess_backupOS_vm
	:param parser: is a dict, get from Test config file
	"""

	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
    						, parser["BackupOS_usr"]
    						, parser["BackupOS_pwd"]) #獲得ssh

	if FTVM.is_running(parser["vm_name"], parser["BackupOS_ip"], ssh):
		print "123"
		time.sleep(float(parser["post_backupOS_wait_VM_enable_shutdown_time"]))
		FTVM.shutdown(parser["vm_name"], parser["BackupOS_ip"], ssh)
	elif FTVM.is_paused(parser["vm_name"], parser["BackupOS_ip"], ssh):
		FTVM.resume(parser["vm_name"], parser["BackupOS_ip"], ssh)
		time.sleep(float(parser["post_backupOS_wait_VM_enable_shutdown_time"]))
		FTVM.shutdown(parser["vm_name"], parser["BackupOS_ip"], ssh)
	time.sleep(float(parser["pos_backupOS_VM_shutdown_time"]))

	'''
	times = 0
	while times < 3 and not FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"], ssh):
		times += 1
		FTVM.shutdown(parser["vm_name"], parser["BackupOS_ip"], ssh)
		time.sleep(float(1))
	'''

	if not FTVM.is_shutoff(parser["vm_name"], parser["BackupOS_ip"], ssh):
		ssh.close()
		raise TA_error.Postprocess_Error("backupOS %s can not shutdown" % parser["vm_name"])

	ssh.close()

def postprocess_hostOS_OS_running(parser):
	"""
	postrocess host OS become running

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_hostOS_OS"] == "yes":
		FTOS.L1_boot(parser["HostOS_NetworkAdaptor"])


def postprocess_backupOS_OS_running(parser):
	"""
	postrocess host OS become running

	:called func: postprocess_hostOS
	:param parser: is a dict, get from Test config file
	"""
	if parser["pos_check_backupOS_OS"] == "yes":
		FTOS.L1_boot(parser["BackupOS_NetworkAdaptor"])

def postprocess_hostOS_ATCA_OS_running(parser):

	if parser["pos_boot_ATCA_hostOS"] == "yes":
		cmd = "ssh 172.16.33.222 'clia activate %s 0'" % (parser["HostOS_ipmc_name"])

		ssh = shell_server.get_ssh(parser["BackupOS_ip"]
							, parser["BackupOS_usr"]
							, parser["BackupOS_pwd"]) #獲得ssh

		s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
		ssh.close()

		if not FTVM.is_login(parser["HostOS_name"]
			, parser["TA_ip"]
			, parser["TA_msg_sock_port"]
			, int(parser["pos_hostOS_login_time"])):
			raise TA_error.Postprocess_Error("HostOS %s is not login" % parser["HostOS_name"])

		#postprocess_hostOS_mount_nfs(parser)


def postprocess_backupOS_ATCA_OS_running(parser):

	if parser["pos_boot_ATCA_backupOS"] == "yes":
		cmd = "ssh 172.16.33.222 'clia activate %s 0'" % (parser["BackupOS_ipmc_name"])

		print cmd

		ssh = shell_server.get_ssh(parser["HostOS_ip"]
    						, parser["HostOS_usr"]
    						, parser["HostOS_pwd"]) #獲得ssh

		s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
		ssh.close()

		if not FTVM.is_login(parser["BackupOS_name"]
			, parser["TA_ip"]
			, parser["TA_msg_sock_port"]
			, int(parser["pos_backupOS_login_time"])):
			raise TA_error.Postprocess_Error("HostOS %s is not login" % parser["BackupOS_name"])

		#postprocess_hostOS_mount_nfs(parser)

def postprocess_hostOS_mount_nfs(parser):

	if parser["pos_hostOS_mount_nfs"] == "yes":
		cmd = "mount -t nfs %s:%s %s" % (parser["nfs_ip"],parser["nfs_share_folder"],parser["local_nfs_path"])

		ssh = shell_server.get_ssh(parser["HostOS_ip"]
						, parser["HostOS_usr"]
						, parser["HostOS_pwd"]) #獲得ssh

		s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
		ssh.close()

if __name__ == '__main__':
	#parser = {}
	#parser["BackupOS_ip"] = "192.168.1.25"
	#parser["BackupOS_usr"] = "user"
	#parser["BackupOS_pwd"] = "pdclab!@#$"
	#parser["vm_name"] = "T01"
	
	parser = {}
	parser["HostOS_ip"] = "192.168.1.100"
	parser["HostOS_usr"] = "primary"
	parser["HostOS_pwd"] = "root"
	#postProcessHostOSReboot(parser)