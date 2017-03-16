import sys
import time
from testagent import TA_error, HAagent
from testagent import process
from testagent import Assert
from testagent import preprocess
from testagent import shell_server


def run_test1(parser):
    preprocess.run_preprocess(parser)
    process.vm_ftstart(parser)
    Assert.vm_running_in_hostOS(parser)
    Assert.vm_is_login_in_hostOS(parser)