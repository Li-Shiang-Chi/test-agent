#!/usr/bin/python
#-*- coding: utf-8 -*-

def command(string):
	"""
	combine command

	:param string: part of command
	:return: mmsh command
	"""
	cmd = "mmsh %s" % string
	return cmd

def overview_cmd():
	"""
	:return cmd: mmsh overview
	"""
	return command("overview")

def infofail_cmd(vm_name):
	"""
	:return cmd: mmsh infofail [vm_name]
	"""
	return command("infofail %s" % vm_name)

def inforecover_cmd(vm_name):
	"""
	:return cmd: mmsh inforecover [vm_name]
	"""
	return command("inforecover %s" % vm_name)

def infohost_cmd(vm_name, option):
	"""
	option: i/n

	:return cmd: mmsh infohost [option] [vm_name]
	"""
	return command("infohost -%s %s" % (option, vm_name))

def statehost_cmd(host_name):
	"""
	:return cmd: mmsh statehost [host_name]
	"""
	return command("statehost %s" % host_name)

def starthost_cmd(host_name):
	"""
	:return cmd: mmsh starthost [host_name]
	"""
	return command("starthost %s" % host_name)

def stophost_cmd(host_name):
	"""
	:return cmd: mmsh stophost [host_name]
	"""
	return command("stophost %s" % host_name)

def startwd_cmd(host_name):
	"""
	:return cmd: mmsh startwd [host_name]
	"""
	return command("startwd %s" % host_name)

def stopwd_cmd(host_name):
	"""
	:return cmd: mmsh stopwd [host_name]
	"""
	return command("stopwd %s" % host_name)

def statewd_cmd(host_name):
	"""
	:return cmd: mmsh statewd [host_name]
	"""
	return command("statewd %s" % host_name)

def stateshmgr_cmd(shmgr_name):
	"""
	:return cmd: mmsh stateshmgr [shmgr_name]
	"""
	return command("shmgr_name %s" % shmgr_name)

def stateipmc_cmd(host_name):
	"""
	:return cmd: mmsh stateipmc [host_name]
	"""
	return command("stateipmc %s" % host_name)

def dangert_cmd(shelf_name):
	"""
	:return cmd: mmsh dangert [shelf_name]
	"""
	return command("dangert %s" % shelf_name)

def dangerv_cmd(shelf_name):
	"""
	:return cmd: mmsh dangerv [shelf_name]
	"""
	return command("dangerv %s" % shelf_name)
def nodanger_cmd(shelf_name):
	"""
	:return cmd: mmsh nodanger [shelf_name]
	"""
	return command("nodanger %s" % shelf_name)

def addshelf_cmd(shelf_ip):
	"""
	:return cmd: mmsh addshelf shm [shelf_ip]
	"""
	return command("addshelf shm %s" % shelf_ip)

def addhost_cmd(host_name, host_ip):
	"""
	:return cmd: mmsh addhost [host_name] [host_ip] shm
	"""
	return command("addhost %s %s shm" % (host_name, host_ip))

def start_vm_in_host_cmd(vm_name, host_name):
	"""
	:return cmd: mmsh start [vm_name] [host_name]
	"""
	return command("mmsh start %s %s" % (vm_name, host_name))

def nopower_cmd(host_name):
	"""
	:return cmd: mmsh nopower [host_name]
	"""
	return command("mmsh nopower %s" % host_name)

def inforole_cmd(host_name):
	"""
	:return cmd: mmsh inforole [host_name]
	"""
	return command("inforole %s" % host_name)
