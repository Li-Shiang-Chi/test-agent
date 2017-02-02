from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_master_monitor_crash(parser):
	"""
	test master monitor crash
	"""
	preprocess.preprocess(parser)
	process.kill_master_monitor_process(parser)
	Assert.master_monitor_running(parser)

