from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_primary_hardware_crash_singleVM_restart(parser):
	"""
		test after node OS crash, vm will restart on another node or not and node's role will change or not
	"""
	#preprocess
	preprocess.preprocess(parser)
	print 401
	#process
	process.exec_L1_hostOS_shutdown(parser)
	print 402
	#assert
	Assert.detect_hostOS_crash(parser)
	print 403
	Assert.vm_running_in_backupOS(parser)
	print 404
	Assert.hostOS_role_is_Slave_on_BackupOS(parser)
	print 405
	Assert.backupOS_role_is_Master_on_BackupOS(parser)
	print 406