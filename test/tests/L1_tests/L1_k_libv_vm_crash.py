from testagent import preprocess
from testagent import process
from testagent import Assert


def run_L1_k_libv_vm_crash(parser):
	"""
	test after ftlibvirt recover, ftlibvirt will detect vm crash or not
	"""
	preprocess.preprocess(parser)

	process.kill_libvirt_process(parser)
	Assert.libvirt_running_in_hostOS(parser)
	
	time.sleep(50)
	process.kill_vm_process(parser)
	Assert.vm_running_in_hostOS(parser)
	Assert.vm_is_login_in_hostOS(parser)
	Assert.detect_fail_vm_crash(parser)
	Assert.recovery_vm_p_restart(parser)