#!/usr/bin/python
#-*- coding: utf-8 -*-

def command(string, ip=""):
	"""
	return virsh command
	"""
	url = ""
	if ip != "":
		url = "-c qemu+tcp://%s/system" % ip
	cmd = "virsh %s %s" % (url, string)
	return cmd

def domstate_cmd(vm_name, ip=""):
	"""
	:param vm_name: vm name
	:param ip: vm's ip
	:return cmd: virsh [url] domstate [vm_name]
	"""
	return command("domstate %s" % vm_name, ip)

def start_cmd(vm_name, ip=""):
	"""
	:param vm_name: vm name
	:param ip: vm's ip
	:return cmd: virsh [url] start [vm_name]
	"""
	return command("start %s" % vm_name, ip)

def ftstart_cmd(vm_name, ip="", level=""):
	"""
	:param vm_name: vm name
	:param ip: vm's ip
	:return cmd: virsh [url] ftstart --level [level] [vm_name]
	"""
	return command("ftstart --level %s %s" % (level, vm_name), ip)

def shutdown_cmd(vm_name, ip=""):
	"""
	:param vm_name: vm name
	:param ip: vm's ip
	:return cmd: virsh [url] shutdown [vm_name]
	"""
	return command("shutdown %s" % vm_name, ip)

def paused_cmd(vm_name, ip=""):
	pass

def resume_cmd(vm_name, ip=""):
	"""
	:param vm_name: vm name
	:param ip: vm's ip
	:return cmd: virsh [url] resume [vm_name]
	"""
	return command("resume %s" % vm_name, ip)