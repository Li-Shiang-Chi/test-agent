#!/usr/bin/python
#-*- coding: utf-8 -*-
import paramiko
import socket
import TA_error


def get_ssh(ip, usr, pwd, t_out=10):
	"""
	get ssh object

	:param ip: ip address
	:param usr: usr name
	:param pwd: use pwd
	:param t_out: ssh time out

	:return ssh: paramiko ssh object
	"""
	try:
		ssh = paramiko.SSHClient() #獲取ssh物件
		ssh.load_system_host_keys() #載入ssh key
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		#print "connecting %s@%s with passwd: %s" % (usr, ip, pwd)
		ssh.connect(ip, username=usr, password=pwd,timeout=t_out) #進行ssh連線
		return ssh
	except paramiko.BadHostKeyException, e:
		print str(e)
		raise TA_error.Shell_server_Error(str(e))
	except paramiko.AuthenticationException, e:
		print str(e)
		raise TA_error.Shell_server_Error(str(e))
	except paramiko.SSHException, e:
		print str(e)
		raise TA_error.Shell_server_Error(str(e))
	except (socket.error, socket.timeout) as e:
		print "socket except : "+str(e)
		raise TA_error.Shell_server_Error(str(e))



if __name__ == "__main__":
	ssh = get_ssh("127.0.0.1" ,
				  "t",
				  "root")
	s_stdin, s_stdout, s_stderr = ssh.exec_command("sudo HAagent overview")
	print "stdout : "+s_stdout.read()
	
	