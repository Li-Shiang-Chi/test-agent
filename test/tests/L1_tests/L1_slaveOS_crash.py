from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L1_slaveOS_crash(parser):
	"""
	general architecture hostOS crash
	"""
	#preprocess
	preprocess.preprocess(parser)
	#process
	process.exec_L1_slaveOS_shutdown(parser)
	#assert
	Assert.vm_running_in_backupOS(parser)
	Assert.vm_is_login_in_backupOS(parser)
	Assert.detect_BackupOS_crash(parser)
	Assert.hostOS_role_is_Master(parser)
	Assert.backupOS_role_is_Slave(parser)