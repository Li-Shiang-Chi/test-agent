from testagent import preprocess
from testagent import process
from testagent import Assert
from testagent import postprocess

def run_HA3_primary_network_isolation(parser):
    """
    general architecture hostOS crash
    """
    #preprocess
    preprocess.preprocess(parser)
    print 401
    #process
    process.exec_primaryOS_network_isolation(parser)
    print 402
    #assert
    Assert.vm_recover_in_backupOS(parser)
    print 404
    Assert.detect_primary_network_isolation_info(parser)
    print 405
    Assert.primaryOS_role_is_slave(parser)
    print 406
    Assert.backupOS_role_is_primary(parser)
    print 407
    