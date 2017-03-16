#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import os
import time
import socket
import threading

class Msg_socket(object):
	"""
	socket for getting message
	"""
	def __init__(self, ip, port, time):
		self.ip = ip
		self.port = port
		self.time = time
		self.socket = None
		self.client = None
		self.msg = None
		self.create()

	def create(self):
		"""
		create socket
		"""
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind((self.ip, int(self.port)))
		self.socket.settimeout(self.time) #設定socket開起時間久
		self.socket.listen(1) #設定該socket只能有一個client連進來

	def open(self):
		"""
		open socket
		"""
		try:
			self.client = self.socket.accept()
			t = threading.Thread(target = self.receive, args=()) #設定用於接收訊息之thread
			t.start()
			t.join()
		except socket.timeout:
			pass
			#print "catch"

	def receive(self):
		self.msg = self.client[0].recv(1024).rstrip()


if __name__ == '__main__':
	sock = Msg_socket("192.168.1.102","20000",10)
	sock.open()
	print sock.msg


