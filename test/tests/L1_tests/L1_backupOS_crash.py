from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_backupOS_crash(parser):
	"""
	general architecture hostOS crash
	"""
	#preprocess
	print 301
	preprocess.preprocess(parser)
	#process
	print 302
	process.exec_L1_backupOS_shutdown(parser)
	#assert
	print 303
	Assert.vm_running_in_hostOS(parser)
	print 304
	Assert.vm_is_login_in_hostOS(parser)
	print 305
	Assert.detect_BackupOS_crash(parser)
	print 306
	Assert.backupOS_role_is_Slave_on_MasterOS(parser)
	print 307