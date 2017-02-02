from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_hostOS_crash(parser):
	"""
	general architecture hostOS crash
	"""
	#preprocess
	preprocess.preprocess(parser)
	print 116
	#process
	process.exec_L1_hostOS_shutdown(parser)
	print 117
	#assert
	Assert.vm_running_in_backupOS(parser)
	print 118
	Assert.vm_is_login_in_backupOS(parser)
	print 119
	Assert.detect_hostOS_crash(parser)
	print 110
	Assert.hostOS_role_is_Slave_on_BackupOS(parser)
	print 111
	Assert.backupOS_role_is_Master_on_BackupOS(parser)
	print 112
