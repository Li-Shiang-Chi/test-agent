#!/usr/bin/python
#-*- coding: utf-8 -*-
import cmd_mmsh
import subprocess
import shell_server

def inforole(host_name, ssh=None):
	"""
	get host role

	:return: master/backup/slave
	"""
	cmd = cmd_mmsh.inforole_cmd(host_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def overview(ssh=None):
	"""
	execute mmsh overview

	:return: screen result 
	"""
	cmd = cmd_mmsh.overview_cmd()

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def infofail(vm_name, ssh=None):
	"""
	execute mmsh infofail [vm_name]

	:param vm_name: vm's name
	:return: screen result 
	"""
	cmd = cmd_mmsh.infofail_cmd(vm_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def inforecover(vm_name, ssh=None):
	"""
	execute mmsh inforecover [vm_name]

	:param vm_name: vm's name
	:return: screen result 
	"""
	cmd = cmd_mmsh.inforecover_cmd(vm_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def infohost(vm_name, option, ssh=None):
	"""
	execute mmsh infohost [option] [vm_name]

	:param vm_name: vm's name 
	:return: host ip/host name
	"""
	cmd = cmd_mmsh.infohost_cmd(vm_name, option)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def statehost(host_name, ssh=None):
	"""
	execute mmsh statehost [host_name]

	:param host_name: host OS name 
	:return: running/initializing/shutdown
	"""
	cmd = cmd_mmsh.statehost_cmd(host_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def starthost(host_name, ssh=None):
	"""
	execute starthost [host_name]

	:param host_name: host OS name 
	:return: success/[nothing]
	"""
	cmd = cmd_mmsh.starthost_cmd(host_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def stophost(host_name, ssh=None):
	"""
	execute stophost [host_name]

	:param host_name: host OS name 
	:return: success/[nothing]
	"""
	cmd = cmd_mmsh.starthost_cmd(host_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def startwd(host_name, ssh=None):
	"""
	execute startwd [host_name]

	:param host_name: host OS name 
	:return: success/[nothing]
	"""
	cmd = cmd_mmsh.startwd_cmd(host_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def stopwd(host_name, ssh=None):
	"""
	execute stopwd [host_name]

	:param host_name: host OS name 
	:return: success/[nothing]
	"""
	cmd = cmd_mmsh.stopwd_cmd(host_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def statewd(host_name, ssh=None):
	"""
	execute statewd [host_name]

	:param host_name: host OS name 
	:return: start/stop
	"""
	cmd = cmd_mmsh.statewd_cmd(host_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def stateshmgr(shmgr_name, ssh=None):
	"""
	execute stateshmgr [shmgr_name]

	:param host_name: host OS name 
	:return: start/stop
	"""
	cmd = cmd_mmsh.statewd_cmd(shmgr_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def stateipmc(host_name, ssh=None):
	"""
	execute stateipmc [ipmc_name]

	:param host_name: host OS name 
	:return: M0~M7
	"""
	cmd = cmd_mmsh.stateipmc_cmd(host_name)

	return remoteExec(cmd, ssh) if ssh else localExec(cmd)

def remoteExec(cmd, ssh):
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #執行指令
	stdout = s_stdout.read()
	return stdout.rstrip()

def localExec(cmd):

	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()
	#print status.rstrip()
	return status.rstrip() 

if __name__ == "__main__":
	"""
	ssh = shell_server.get_ssh("140.115.53.132","user","")
	print overview(ssh)
	"""