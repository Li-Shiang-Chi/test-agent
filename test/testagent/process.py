#/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess
import data_dir
import FTsystem
import FTVM
import cmd_kill
import shell_server
import mmsh
import master_monitor
import time
import HAagent
import TA_error
from testagent import cmd_HAagent

def exec_L1_backupOS_network_isolation(parser):

	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh

	cmd = "sudo ifdown %s && sudo sleep 150s && sudo ifup %s" % (parser["BackupOS_network_interface"], parser["BackupOS_network_interface"] )
	print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()

def exec_L1_hostOS_network_isolation(parser):

	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh

	cmd = "sudo ifdown %s && sudo sleep 180s && sudo ifup %s" % (parser["HostOS_network_interface"], parser["HostOS_network_interface"] )
	print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()


def exec_L1_slaveOS_shutdown(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["slaveOS_ip"]
                              , parser["slaveOS_usr"]
                              , parser["slaveOS_pwd"]) #獲得ssh
	cmd = "sudo poweroff -f" 
	#print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()

def exec_L1_backupOS_shutdown(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
	cmd = "sudo poweroff -f" 
	#print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()

def exec_L1_hostOS_networkIsolation(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	cmd = "cd /home/user;sudo ./testif.sh;" 
	#print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()

def exec_L1_hostOS_shutdown(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	print 77
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	print 78
	cmd = "sudo poweroff -f" 
	print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()
	print 79
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	print 80

def exec_L1_hostOS_crasher(parser):
	"""
	execute level 1 crasher in hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	cmd = "sudo "+cmd_kill.kill_cmd(1,11) #獲得kill -SIGSEGV 1之指令字串
	#print cmd 
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	#print "stdout",s_stdout.read()
	#print "stderr",s_stderr.read()
	ssh.close()
	"""
	#Another way to crash
	
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"])
	f_path = parser["HostOS_process_dir"]+"L1_crasher"
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd)
	ssh.close()
	"""

def kill_vm_process(parser):
	"""
	kill vm process on hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_kill_vm_p" in parser.keys(): #若pro_wait_time_kill_vm_p存在於parser
		time.sleep(int(parser["pro_wait_time_kill_vm_p"]))
	#print "kill"

	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	pid = FTVM.get_pid(parser["vm_name"], parser["HostOS_ip"], ssh) #獲得VM之pid
	cmd = cmd_kill.kill_cmd(pid, 9) #獲得kill vm process之指令字串
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #透過ssh執行指令
	ssh.close()

def kill_libvirt_process(parser):
	"""
	kill libvirt process on hostOS

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_kill_libvirt_p" in parser.keys(): #若pro_wait_time_kill_libvirt_p存在於parser
		time.sleep(int(parser["pro_wait_time_kill_libvirt_p"]))

	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	pid = FTsystem.get_pid(ssh) #透過ssh獲得libvirt之pid
	if pid == False:
		ssh.close()
		raise TA_error.Process_Error("can not get libvirt pid")
	cmd = cmd_kill.kill_cmd(pid, 9) #獲得kill libvirt process之指令字串
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #透過ssh執行指令
	ssh.close()
	
def kill_master_monitor_process(parser):
	"""
	kill master monitor process on hostOS

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh

	if "pro_wait_time_kill_mm_p" in parser.keys(): #若pro_wait_time_kill_mm_p存在於parser
		time.sleep(int(parser["pro_wait_time_kill_mm_p"]))
	
	pid = master_monitor.get_pid(ssh) #獲得master monitor之pid
	if pid == False:
		raise TA_error.Process_Error("can not get master monitor pid")
	print pid
	cmd = "sudo "+cmd_kill.kill_cmd(pid, 9) #獲得kill master monitor process之指令字串
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo "+cmd) #透過ssh執行指令
	#subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate() #執行指令
	ssh.close()

def exec_L1_vm_crasher(parser):
	"""
	execute level 1 crasher in vm 
	kill init process

	:param parser: is a dict, get from Test config file
	"""
	if "pro_wait_time_exe_L1_crasher" in parser.keys(): #若pro_wait_time_exe_L1_crasher存在於parser
		time.sleep(int(parser["pro_wait_time_exe_L1_crasher"]))
	
	ssh = shell_server.get_ssh(parser["GuestOS_ip"]
                              , parser["GuestOS_usr"]
                              , parser["GuestOS_pwd"]) #獲得ssh
	cmd = "sudo "+cmd_kill.kill_cmd(1,11) #獲得kill -SIGSEGV 1之指令字串
	#print cmd
	s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd) #透過ssh執行指令
	ssh.close()

def vm_start(parser):
	"""
	normaly start vm

	:param parser: is a dict, get from Test config file
	"""


	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh

	if "pro_wait_time_start" in parser.keys():
		time.sleep(int(parser["pro_wait_time_start"]))	

	FTVM.start(parser["vm_name"], parser["HostOS_ip"],ssh)

	ssh.close()

def vm_ftstart(parser):
	"""
	ftstart vm

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh

	if "pro_wait_time_start" in parser.keys():
		time.sleep(int(parser["pro_wait_time_start"]))
	
	FTVM.ftstart(parser["vm_name"], parser["HostOS_ip"], parser["level"],ssh) #執行開啟容錯機制之開機
	ssh.close()

def vm_shutdown(parser):
	"""
	shutdown vm

	:param parser: is a dict, get from Test config file
	"""
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh

	if "pro_wait_time_shutdown" in parser.keys():
		time.sleep(int(parser["pro_wait_time_shutdown"]))
	
	FTVM.shutdown(parser["vm_name"], parser["HostOS_ip"],ssh)
	ssh.close()
	
	"""
	HAagent create cluster
	:param parser: is a dict, get from Test config file
	"""
	
def exec_create_cluster(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh

	HAagent.create_cluster(parser["Cluster_name"], parser["HostOS_name"], parser["HostOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	ssh.close()
	
	"""
	HAagent create duplicate cluster
	:param parser: is a dict, get from Test config file
	"""	

def exec_create_duplicate_cluster(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh

	HAagent.create_cluster(parser["Cluster_name"], parser["HostOS_name"], parser["HostOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	ssh.close()
	
	"""
	HAagent delete cluster
	:param parser: is a dict, get from Test config file
	"""	

def exec_de_cluster(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster(parser["Cluster_name"], parser["HostOS_name"], parser["HostOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	HAagent.de_cluster(parser["Cluster_name"], parser, ssh)
	ssh.close()
	
	"""
	HAagent external cluster primary delete cluster
	:param parser: is a dict, get from Test config file
	"""

def exec_de_outer_cluster(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster("test_b", "test_n", "9999", "9999", parser, ssh)
	HAagent.de_cluster(parser["Cluster_name"], parser, ssh)
	ssh.close()
	
	"""
	HAagent add node to cluster
	:param parser: is a dict, get from Test config file
	"""
	
def exec_non_primary_de_cluster(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh

	HAagent.create_cluster(parser["Cluster_name"], parser["HostOS_name"], parser["HostOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	HAagent.add_backup_node(parser , ssh)
	time.sleep(float(1))
	
	ssh.close()
	ssh = shell_server.get_ssh(parser["BackupOS_ip"]
                              , parser["BackupOS_usr"]
                              , parser["BackupOS_pwd"]) #獲得ssh
	
	HAagent.de_cluster(parser["Cluster_name"], parser, ssh)
	
	ssh.close()
	
def exec_add_node(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster(parser["Cluster_name"], parser["HostOS_name"], parser["HostOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	time.sleep(3)
	#HAagent.add_backup_node(parser , ssh) # add backup node
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo mmsh addnode test_c backup 192.168.1.101 86 && sudo sleep 2s")
	time.sleep(float(parser["pro_wait_add_node_time"])) 
	print s_stdout.read()
	#HAagent.add_slave_node(parser , ssh) #add slave node
	#time.sleep(float(parser["pro_wait_add_node_time"])) 
	ssh.close()
	
	"""
	HAagent add duplicate node to cluster
	:param parser: is a dict, get from Test config file
	"""
	
def exec_add_duplicate_node(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster(parser["Cluster_name"], parser["HostOS_name"], parser["HostOS_ipmb"], parser["Shelf_ip"], parser, ssh) 
	time.sleep(1)
	ssh.close()
	
	"""
	HAagent add outer node to cluster
	:param parser: is a dict, get from Test config file
	"""
	
def exec_add_outer_node(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster(parser["Cluster_name"], parser["HostOS_name"], parser["HostOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	time.sleep(1)
	ssh.close()
	
	"""
	HAagent remove node in cluster
	:param parser: is a dict, get from Test config file
	"""
	
def exec_de_node(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	HAagent.create_cluster(parser["Cluster_name"], parser["HostOS_name"], parser["HostOS_ipmb"], parser["Shelf_ip"], parser, ssh)
	time.sleep(1)
	HAagent.rm_node(parser["Cluster_name"], parser["HostOS_name"], parser, ssh)
	time.sleep(1)
	ssh.close()
	
	"""
	HAagent remove outer node
	:param parser: is a dict, get from Test config file
	"""
	
def exec_de_outer_node(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	ssh.close()
	"""
	HAagent overview
	:param parser: is a dict, get from Test config file
	"""
	
def exec_overview(parser):
	ssh = shell_server.get_ssh(parser["HostOS_ip"]
                              , parser["HostOS_usr"]
                              , parser["HostOS_pwd"]) #獲得ssh
	
	HAagent.quick_create_cluster(parser, ssh)
	time.sleep(1)
	ssh.close()
    
if __name__ == '__main__':
	parser = dict()
	parser["HostOS_ip"] = "140.115.53.132"
	parser["HostOS_network_interface"] = "br0"
	exec_L1_hostOS_network_isolation(parser)
