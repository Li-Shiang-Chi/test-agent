#!/usr/bin/python
#-*- coding: utf-8 -*-
import paramiko
import data_dir
import cmd_service
import cmd_egrep
import mmsh

"""
FTsystem is libvirt-bin
"""

def get_status(ssh):
	"""
	get FTsystem status
	:param ssh: ssh object 
				use to send command
	:return: running/not running
	"""
	cmd = cmd_egrep.ssh_extract_pid_cmd(cmd_service.status_cmd("libvirt-bin")) #獲得透過egrep抓取pid的指令字串
	cmd = "sudo %s" % cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #執行指令
	if s_stdout.read() == "": #沒抓取到任何pid，則進入，表示不在執行之狀態
		print "FTsystem not running"
		#return "not running"
	return "running"

def is_running(ssh):
	"""
	libvirt is running or not

	:param ssh: ssh object 
				use to send command
	:return: True / False
	"""
	if get_status(ssh) == "running":
		return True
	return False

def start(ssh):
	"""
	start FTsystem

	:param ssh: ssh object 
				use to send command
	"""
	cmd = cmd_service.start_cmd("libvirt-bin") #獲得service start [process name]的指令字串
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
	print s_stdout.read()

def stop(ssh):
	"""
	stop FTsystem

	:param ssh: ssh object 
				use to send command
	"""
	cmd = cmd_service.stop_cmd("libvirt-bin") #獲得service stop [process name]的指令字串
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
	print s_stdout.read()

def get_pid(ssh):
	"""
	get libvirt pid

	:param ssh: ssh object 
				use to send command
	:return: pid/False(get no pid)
	"""
	pid_file_path = data_dir.LIBVIRT_PID_DIR+"libvirtd.pid" #獲得libvirtd.pid檔案的路徑
	cmd = "sudo cat %s" % pid_file_path #組合cat指令
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #執行指令
	pid = s_stdout.read()
	if pid != "":
		return int(pid)
	return False
