
from testagent import Assert
from testagent import preprocess


def run_L3_non_primary_rm_ftvm(parser):
    preprocess.run_preprocess(parser)
    Assert.non_primary_rm_ftvm(parser)