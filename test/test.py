#! /usr/bin/env python

import subprocess

b = "node"
c = "vm"
d = "vm node"


a = {
	'b' : "123",
	'c' : "456",
	'd' : "789"
}


if __name__ == '__main__':
	cmd = "bash initAll.sh >> init.out"
	status, error = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE , cwd="/home/slave/Desktop/HATest/test-agent/test/").communicate()