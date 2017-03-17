#!/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess



def get_process_id(string):
	return "ps -ef | grep %s | awk '{if(NR==1) print $2}'" % string

def command(string):
	"""
	combine command

	:param string: part of command
	:return: egrep command
	"""
	cmd = "egrep %s" % string
	return cmd

def ssh_extract_pid_cmd(cmd):
	"""
	ssh extract pid by egrep

	:param cmd: part of command
	:return new_cmd: command is combined
	"""
	grep_cmd = command("-oi 'running'") 
	"""
	origin cmd :grep -oi '([0-9]+)$'
	if you want use subprocess.Popen to run cmd you must to change '([0-9]+)$' to ([0-9]+)$
	"""
	new_cmd = "%s | %s" % (cmd, grep_cmd)
	return new_cmd

def extract_pid_cmd():
	"""
	extract pid by egrep

	:param cmd: part of command
	:return new_cmd: command is combined
	"""
	grep_cmd = command("-oi ([0-9]+)$") 
	return grep_cmd


if __name__ == '__main__':
	cmd = extract_pid_cmd("service libvirt-bin status")
	print cmd
	output, error = subprocess.Popen("service libvirt-bin status".split(), stdout=subprocess.PIPE).communicate()
	print output
	#output = subprocess.check_output("service libvirt-bin status | egrep -oi '([0-9]+)$'", shell=True, stderr=subprocess.STDOUT,)
	#print "output: "+output
	p1 = subprocess.Popen("service libvirt-bin status".split(), stdout=subprocess.PIPE)
	#p2 = subprocess.Popen(["egrep","-oi", "([0-9]+)$"], stdin=p1.stdout, stdout=subprocess.PIPE)
	p2 = subprocess.Popen("egrep -oi ([0-9]+)$".split(), stdin=p1.stdout, stdout=subprocess.PIPE)
	p1.stdout.close()
	print p2.communicate()[0].rstrip()
	

