from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_ft_libvirt_crash(parser):
	"""
	test ft libivrt crash
	"""
	preprocess.preprocess(parser)
	process.kill_libvirt_process(parser)
	Assert.libvirt_running_in_hostOS(parser)