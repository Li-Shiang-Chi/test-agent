from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_HA3_primaryOS_crash(parser):
    """
    general architecture hostOS crash
    """
    preprocess.run_preprocess(parser)
    print 116
    #process
    process.exec_primaryOS_shutdown(parser)
    print 117
    #assert
    Assert.vm_recover_in_backup_or_slave(parser)
    print 119
    #Assert.detect_primaryOS_crash(parser)
    #Assert.detect_primaryOS_crash_info(parser)
    print 110
    Assert.primaryOS_role_is_slave(parser)
    print 111
    Assert.backupOS_role_is_primary(parser)
    print 112
    Assert.slaveOS_role_is_backup(parser)
    print 113