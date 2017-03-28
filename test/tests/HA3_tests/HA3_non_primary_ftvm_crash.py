from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_HA3_non_primary_ftvm_crash(parser):
    
    preprocess.run_preprocess(parser)
    print 110
    process.kill_backup_vm_process(parser)
    print 111
    Assert.vm_recover_in_backupOS(parser)
    print 113
    Assert.detect_backup_vm_crash_info(parser)