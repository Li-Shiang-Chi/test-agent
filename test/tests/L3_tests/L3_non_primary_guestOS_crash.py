from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_L3_non_primary_guestOS_crash(parser):
    
    preprocess.run_preprocess(parser)
    print 110
    process.exec_vm_guestOS_crasher(parser)
    print 111
    Assert.vm_running_in_BackupOS(parser)
    print 112
    Assert.vm_is_login_in_BackupOS(parser)
    print 115
    Assert.detect_primary_vm_guestOS_hang_info(parser)