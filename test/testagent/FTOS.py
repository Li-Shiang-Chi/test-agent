#!/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess
import time
import data_dir
import shell_server
import mmsh
import os
import TA_error

def HostOSIsRunning(parser):
	"""
	use ping to check host os is running
	:param parser : parser: is a dict, get from Test config file
	"""
	if("pre_wait_node_os_shutdown_time" in parser.keys()):
		time.sleep(float(parser["pre_wait_node_os_shutdown_time"]))
	t_start = time.time()
	while ( (time.time() - t_start) < parser["pre_hostOS_boot_time"] ) :
		response = os.system("ping -c 1 " + parser["HostOS_ip"])
		print 'host os ping response %s' % response
		if response == 0:
			return True;
		time.sleep(float(1))
	return False

def BackupOSIsRunning(parser):
	"""
	use ping to check backup os is running
	:param parser : parser: is a dict, get from Test config file
	"""
	if("pre_wait_node_os_shutdown_time" in parser.keys()):
		time.sleep(float(parser["pre_wait_node_os_shutdown_time"]))
	t_start = time.time()
	while ( (time.time() - t_start) < parser["pre_backupOS_boot_time"] ) :
		response = os.system("ping -c 1 %s" % parser["BackupOS_ip"])
		print 'backup os ping response %s' % response
		if response == 0: # node can ping
			return True;
		time.sleep(float(1))
	return False

def SlaveOSIsRunning(parser):
	"""
	use ping to check slave os is running
	:param parser : parser: is a dict, get from Test config file
	"""
	if("pre_wait_node_os_shutdown_time" in parser.keys()):
		time.sleep(float(parser["pre_wait_node_os_shutdown_time"]))
	t_start = time.time()
	while ( (time.time() - t_start) < parser["pre_slaveOS_boot_time"] ) :
		response = os.system("ping -c 1 " + parser["SlaveOS_ip"])
		if response == 0:	
			return True;
		time.sleep(float(1))
	return False

def NFSOSIsRunning(parser):
	"""
	use ping to check nfs os is running
	:param parser : parser: is a dict, get from Test config file
	"""
	if("pre_wait_node_os_shutdown_time" in parser.keys()):
		time.sleep(float(parser["pre_wait_node_os_shutdown_time"]))
	t_start = time.time()
	while ( (time.time() - t_start) < parser["pre_backupOS_boot_time"] ) :
		response = os.system("ping -c 1 %s" % parser["BackupOS_ip"])
		print 'nfs os ping response %s' % response
		if response == 0: # node can ping
			return True;
		time.sleep(float(1))
	return False

def HostOS_SSH_Is_Ready(parser):
	t_start = time.time()
	while( (time.time() - t_start) < parser["pre_wait_ssh_time"]):
		ssh_response = os.system("nc -z %s 22 >/dev/null" % parser["HostOS_ip"])
		print 'host os ssh response %s' % ssh_response
		if ssh_response == 0:
			return True
		time.sleep(float(1))
	return False

def BackupOS_SSH_Is_Ready(parser):
	t_start = time.time()
	while( (time.time() - t_start) < parser["pre_wait_ssh_time"]):
		ssh_response = os.system("nc -z %s 22 >/dev/null" % parser["BackupOS_ip"])
		print 'backup os ssh response %s' % ssh_response
		if ssh_response == 0:
			return True
		time.sleep(float(1))
	return False
def SlaveOS_SSH_Is_Ready(parser):
	t_start = time.time()
	while( (time.time() - t_start) < parser["pre_wait_ssh_time"]):
		ssh_response = os.system("nc -z %s 22 >/dev/null" % parser["SlaveOS_ip"])
		if ssh_response == 0:
			return True
		time.sleep(float(1))
	return False
def NFSOS_SSH_Is_Ready(parser):
	t_start = time.time()
	while( (time.time() - t_start) < parser["pre_wait_ssh_time"]):
		ssh_response = os.system("nc -z %s 22 >/dev/null" % parser["NFS_ip"])
		if ssh_response == 0:
			return True
		time.sleep(float(1))
def wakeUpNode(networkMAC):
	"""
	use wake on lan to boot specific node
	:param networkMAC : network card MAC address
	"""
	cmd = "wakeonlan %s" %  networkMAC
	print cmd
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	

def get_OS_status(OS_name):
	"""
	get OS status

	status : running / shutdown / initializing
	:param os_name: host OS name
	:return status : running / shutdown / initializing
	"""
	return mmsh.statehost(OS_name).rstrip()

def is_running(OS_name):
	"""
	ask OS is running or not

	:param os_name: host OS name
	:return: True (if OS is running)/False (if OS isn't running)
	"""
	if get_OS_status(OS_name) == "running":
		return True
	return False

def is_shutdown(OS_name):
	"""
	ask OS is running or not

	:param os_name: host OS name
	:return: True (if OS is shutdown)/False (if OS isn't shutdown)ATCA
	"""
	if get_OS_status(OS_name) == "shutdown":
		return True
	return False

def boot(OS_name):
	"""
	boot OS

	:param os_name: host OS name
	:return: success / [nothing]
	"""
	return mmsh.starthost(OS_name)

def shutdown(OS_name):
	"""
	shutdown OS

	:param os_name: host OS name
	:return: success / [nothing]
	"""
	return mmsh.stophost(OS_name)


def L1_boot(Network_adaptor_phy_address):
	"""
	boot L1 OS

	:param os_name: Network adaptor Physical address
	:return: success / [nothing]
	"""
	cmd = "wakeonlan %s" %  Network_adaptor_phy_address
	print cmd
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
	#print error

def is_login(host_name, ip, port, time=60):
	"""
	host is login or not

	:param host_name: host name
	:param ip:host's  ip
	:param time: socket open time
	return True (if host is login)/False(else)
	"""
	import datetime
	import time as t
	sock = msg_socket.Msg_socket(ip, port, time) #設定socket
	sock.open() #開啟socket
	#print sock.msg
	if (host_name+" login") == sock.msg: 
		st = datetime.datetime.fromtimestamp(t.time()).strftime('%Y-%m-%d %H:%M:%S')
                #print "[%s][FTVM] VM %s:%s is logged in." % (st, vm_name, ip)
		return True
	return False
if __name__ == "__main__":
	parser = {}
	parser["pre_hostOS_boot_time"] = "200"
	parser["HostOS_ip"] = "192.168.1.100"
	HostOSIsRunning(parser)