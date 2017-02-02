import sys
import time
from testagent import TA_error, HAagent
from testagent import process
from testagent import Assert
from testagent import preprocess
from testagent import shell_server


def run_test1(parser):
    raise TA_error.Assert_Error("test1 assert exception")
    time.sleep(float("2.333"))
  #ssh = shell_server.get_ssh(parser["HostOS_ip"]
   #                           , parser["HostOS_usr"]
   #                           , parser["HostOS_pwd"]) #獲得ssh 
  #HAagent.clear_cluster(parser, ssh)
    raise TA_error.Assert_Error("test1 assert exception")
    return True