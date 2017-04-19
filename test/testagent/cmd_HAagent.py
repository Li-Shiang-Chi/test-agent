'''
@author: lsc

this is a class which will generate the HA3.0 command.
'''

def create_cluster_cmd (cluster_name , node_name , ibmp=None , shelf_ip=None):
    return "mmsh createcluster %s %s %s %s" % (cluster_name , node_name , ibmp , shelf_ip)

def de_cluster_cmd (cluster_name):
    return "mmsh decluster %s" % cluster_name

def add_node_cmd (cluster_name , node_name , node_ip=None , ibmp=None):
    return "mmsh addnode %s %s %s %s" % (cluster_name , node_name , node_ip , ibmp)

def rm_node_cmd (cluster_name , node_name):
    return "mmsh rmnode %s %s" % (cluster_name , node_name)

def start_ftvm_cmd (node_name , vm_name , xml_path=None):
    if xml_path:
        return "mmsh startftvm %s %s %s" % (node_name , vm_name , xml_path)
    return "mmsh startftvm %s %s" % (node_name , vm_name)

def remove_ftvm_cmd(vm_name):
    return "mmsh removeftvm %s" % (vm_name)

def overview_cmd():
    return "mmsh overview"

def get_pid_cmd():
    return "ps -ef | grep HAAgent.py | awk '{if(NR==1) print $2}'"

def exit_cmd():
    return "mmsh exit"

if __name__ == "__main__":
    print create_cluster_cmd("123", "234")
    print de_cluster_cmd("123")
    print add_node_cmd("123", "234")
    print rm_node_cmd("123", "234")
    print start_ftvm_cmd("123", "234" , "213123")
    print remove_ftvm_cmd("123")
    print overview_cmd()
    print exit_cmd()