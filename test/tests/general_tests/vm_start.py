from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_vm_start(parser):
	"""
	test vm start 
	"""
	#preprocess
	print 111
	preprocess.preprocess(parser)
	#process
	print 112
	process.vm_start(parser)
	#assert
	print 113
	Assert.vm_running_in_hostOS(parser)
	print 114
	Assert.vm_is_login_in_hostOS(parser)
	print 115
