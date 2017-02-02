#!/usr/bin/python
#-*- coding: utf-8 -*-

def kill_cmd(pid ,sig_no = "15"):
	"""
	kill [sig_no] [pid]

	:param pid: kill process pid
	:param sig_no: kill signal
	:return: kill command
	"""
	return "kill -%s %s" % (sig_no, pid)