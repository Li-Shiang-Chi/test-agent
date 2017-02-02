from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_a_hostOS_crash(parser):
	"""
	test atca architecture hostOS crash
	"""

	#preprocess
	preprocess.preprocess(parser)
	print 206
	#process
	process.exec_L1_hostOS_crasher(parser)
	print 207
	#assert
	Assert.vm_running_in_backupOS(parser)
	print 208
	Assert.vm_is_login_in_backupOS(parser)
	print 209
	Assert.detect_fail_os_crash(parser)
	print 210
	Assert.recovery_vm_reboot(parser)
	print 211
	Assert.hostOS_status_is_running(parser)
	print 212