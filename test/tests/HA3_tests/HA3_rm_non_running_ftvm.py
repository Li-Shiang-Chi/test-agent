from testagent import process
from testagent import Assert
from testagent import preprocess


def run_HA3_rm_non_running_ftvm(parser):
    preprocess.run_preprocess(parser)
    Assert.detect_rm_non_running_ftvm(parser)
    