from testagent import process
from testagent import Assert
from testagent import preprocess


def run_HA3_primary_start_duplicate_ftvm(parser):
    preprocess.run_preprocess(parser)
    process.host_vm_ftstart(parser)
    Assert.vm_duplicate_start(parser)
    Assert.vm_recover_in_primaryOS(parser)