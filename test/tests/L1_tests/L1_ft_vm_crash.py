from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_ft_vm_crash(parser):
	"""
	test level 1 fault tolerant VM crash
	"""
	print 110
	preprocess.preprocess(parser)
	print 111
	process.kill_vm_process(parser)
	print 112
	Assert.vm_running_in_hostOS(parser)
	print 113
	Assert.vm_is_login_in_hostOS(parser)
	print 114
	#Assert.detect_fail_vm_crash(parser)
	print 115
	#Assert.recovery_vm_p_restart(parser)
	print 116
	