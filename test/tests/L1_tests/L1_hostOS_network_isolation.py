from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_hostOS_network_isolation(parser):
	"""
	general architecture hostOS crash
	"""
	#preprocess
	preprocess.preprocess(parser)
	print 401
	#process
	process.exec_L1_hostOS_network_isolation(parser)
	print 402
	#assert
	Assert.vm_running_in_backupOS(parser)
	print 403
	Assert.detect_hostOS_crash(parser)
	print 404
	Assert.hostOS_role_is_Slave_on_BackupOS(parser)
	print 405
	Assert.backupOS_role_is_Master_on_BackupOS(parser)
	print 406