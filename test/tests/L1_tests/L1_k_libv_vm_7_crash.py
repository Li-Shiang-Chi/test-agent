from testagent import preprocess
from testagent import process
from testagent import Assert
import time


def run_L1_k_libv_vm_7_crash(parser):
	"""
	test after ftlibvirt recover, ftlibvirt will detect vm crash or not
	"""
	preprocess.preprocess(parser)
	
	for i in range(3): 
		process.kill_libvirt_process(parser)
		print 110
		Assert.libvirt_running_in_hostOS(parser)
		print 111
		print "Start killing  process"	
		start_time = time.time()
		last_end = start_time
		time.sleep(50)
		for i in range(1 + 3 * i):
			print 112
			process.kill_vm_process(parser)
			print 113
			Assert.vm_running_in_hostOS(parser)
			print 114
			Assert.vm_is_login_in_hostOS(parser)
			print 115
			Assert.detect_fail_vm_crash(parser)
			print 116
			Assert.recovery_vm_p_restart(parser)
			print 117
			end_time = time.time()
			print "[%f] %dth time kill VM process, ellapsed time %f" % (end_time - start_time, i, end_time - last_end)
			last_end = end_time
