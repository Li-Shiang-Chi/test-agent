from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_backupOS_network_isolation(parser):
	"""
	general architecture hostOS crash
	"""
	#preprocess
	preprocess.preprocess(parser)
	print 11
	#process
	process.exec_L1_backupOS_network_isolation(parser)
	print 12
	#assert
	Assert.vm_running_in_hostOS(parser)
	print 1
	Assert.vm_is_login_in_hostOS(parser)
	print 2
	Assert.detect_hostOS_crash(parser)
	print 3
	Assert.backupOS_role_is_Slave_on_MasterOS(parser)
	print 4
	Assert.hostOS_role_is_Master(parser)
	print 5