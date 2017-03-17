from testagent import process
from testagent import Assert
from testagent import preprocess


def run_L3_primary_rm_ftvm(parser):
    preprocess.run_preprocess(parser)
    process.host_vm_ftshutdown(parser)
    Assert.vm_shudown_in_hostOS(parser)