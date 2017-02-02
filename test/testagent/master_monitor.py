#!/usr/bin/python
#-*- coding: utf-8 -*-
import data_dir
import cmd_service
import cmd_egrep
import shell_server
import subprocess


def get_status(ssh):
	"""
	get FTsystem status

	:return: running/not running
	"""
	cmd = cmd_service.status_cmd("master_monitord") #獲得service [process name] status 之指令字串
	cmd = "sudo %s" % cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	result = s_stdout.read()
	#result = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE) #指行指令
	cmd = cmd_egrep.extract_pid_cmd() #獲得egrep抓取pid之指令字串
	p = subprocess.Popen(cmd.split(),  stdin=subprocess.PIPE, stdout=subprocess.PIPE) #執行指令
	p.stdin.write(result)
	pid = p.communicate()[0]
	#print pid
	if pid == "":
		return "not running"
	return "running"

def is_running(ssh):
	"""
	master monitor is running or not

	:return: True / False
	"""
	if get_status(ssh) == "running":
		return True
	return False

def get_pid(ssh):
	"""
	get master monitor pid

	:return: pid/ False(get no pid)
	"""

	pid_file_path = data_dir.MM_PID_DIR+"master_monitord.pid" #獲得master_monitord.pid之檔案路徑
	cmd = "sudo cat %s" % pid_file_path #組合cat指令
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	return s_stdout.read()
	#pid, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令
	#if error == None:
	#	return int(pid)
	#return False


def temp_start():
	"""
	temp start for master monitor
	"""
	sh_file_path = data_dir.ROOT_DIR+"mm_initial.sh"
	cmd = "sudo %s" % sh_file_path
	subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()