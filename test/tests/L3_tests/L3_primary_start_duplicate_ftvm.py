from testagent import process
from testagent import Assert
from testagent import preprocess


def run_L3_primary_start_duplicate_ftvm(parser):
    preprocess.run_preprocess(parser)
    process.host_vm_ftstart(parser)
    Assert.vm_running_in_hostOS(parser)
    Assert.vm_is_login_in_hostOS(parser)
    Assert.vm_duplicate_start(parser)