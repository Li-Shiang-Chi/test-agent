from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L3_guestOS_crash(parser):
    
    preprocess.run_preprocess(parser)
    print 110
    process.exec_L1_vm_crasher(parser)
    print 111
    Assert.vm_running_in_hostOS(parser)
    print 112
    Assert.vm_is_login_in_hostOS(parser)
    print 113
    #Assert.detect_fail_os_crash(parser)
    print 114
    #Assert.recovery_vm_reboot(parser)
    print 115
    Assert.detect_host_vm_guestOS_hang_info(parser)