#!/usr/bin/env python
import libvirt

'''
this is a configure file for all module in HAagent

Configure
@author:liyanlin
time:2016/9/19
'''
# if node support ipmi or not
Ipmi_supported = False

# this part is used in clusterInfo
# the path of folder which has nfs file in it
Nfs_file_folder_path = "nfsFileFolder"
# in nfs mount folder, the name of folder which has node info file in it
Node_file_folder_name = "nodeFileFolder"
# nfs file's name
Nfs_file_name = "nfsFile"
# clusterInfo file's name
Cluster_file_name = "clusterFile"
# nfs file content
Nfs_ip = "nfs_ip"
Nfs_path = "nfs_folder_path"
File_type_txt = ".txt"
Wrong_self_ip_format = "127."
# the role of node
Primary_role = 0
Backup_role = 1
Node_role = 2
# variable name list for clusterInfo
Clusterinfo_variable_name_list = ["cluster_name", "shelf_ip", "nodes", "my_Node_name"]
# the ip address of DNS server that used to get self ip address
Dns_server_ip = "8.8.8.8"
Get_ip_port = 80

# this part is used in nodeInfo
# variable name list for nodeInfo
Nodeinfo_variable_name_list = ["node_ip", "role", "ibmp", "last_fail", "vms"]

# this part is used in vmInfo
# variable name list for vmInfo
Vminfo_variable_name_list = ["last_fail"]

# socket information
CommandHandler_port = 6666
VMManager_port = 6667
Connect_timeout = 5

# this part is used in CommandHandler
# command title
Command_createcluster = "createcluster"
Command_addnode = "addnode"
Command_rmnode = "rmnode"
Command_decluster = "decluster"
Command_overview = "overview"
Command_startftvm = "startftvm"
Command_removeftvm = "removeftvm"
Command_joincluster = "joincluster"
Command_leavecluster = "leavecluster"
Command_becomeprimary = "becomeprimary"
# VMManager command title
Command_check_domain_running = "eheckDomainRunning"
Command_start_vm = "startVM"
Command_shutdown_vm = "shutdownVM"
Command_reboot_vm = "rebootVM"
Command_update_vm_status = "updateVMStatus"
Invalid_command = "this is invalid command"

# command format
# joincluster cluster_name node_name
Joincluster_command_format = Command_joincluster + " %s %s"
Leavecluster_command_format = Command_leavecluster
Becomeprimary_command_format = Command_becomeprimary
# add vm_name to command tail
Checkdomainrunning_command_format = Command_check_domain_running + " %s"
Startvm_command_format = Command_start_vm + " %s"
Shutdownvm_command_format = Command_shutdown_vm + " %s"
Rebootvm_command_format = Command_reboot_vm + " %s"
Update_vm_status_command_format = Command_update_vm_status + " %s %s"

# CommandHandler success message
Create_cluster_success = "create cluster success"
Decluster_success = "decluster success"
Add_node_success = "add node success"
Closeftvm_success = "close %s success"
Startftvm_success = "add %s in %s success"
Rmnode_success = "remove %s success"
Joincluster_success = "join cluster successfully"
Leavecluster_success = "leave cluster successfully"
Becomeprimary_success = "become primary successfully"
Rmnode_success_2 = "because there is only this node in cluster, System decluster directly"
Startvm_success = "start vm successfully"
Shutdownvm_success = "shutdown vm successfully"
Rebootvm_success = "reboot vm successfully"
Update_vm_status_success = "update vm status successfully"

# CommandHandler failed message
Startvm_create_vm_failed = "failed to start vm and add vm into cluster file, the result is: %s"
Startvm_addVM_failed = "start vm successfully, but failed to add vm into cluster file, the result is: %s"
Shutdownvm_destroy_vm_failed = "failed to shutdown vm and remove vm from cluster file, the result is: %s"
Shutdownvm_rmVM_failed = "shutdown vm successfully, but remove vm from cluster file, the result is: %s"
Checking_vm_running_failed = "failed to check vm running on node(%s), the failed result is: %s"

# file or folder information error messages
Nfs_folder_not_exist = "nfs folder doesn't exist or is empty"
Nfs_file_not_exist = "can not found nfs file, please check it exist"
Nfs_file_content_error = "can not found nfs ip or mounting folder path in nfs file"
Mounting_folder_not_exist = "nfs mounting folder dosen't exist"
Node_file_not_exist = "node file doesn't exist or is empty"
Cluster_file_not_exist = "cluster file doesn't exist or is empty"

# Cluster operation error messages
Init_cluster_info_failed = "initialize clusterInfo failed"
Cluster_name_not_match = "cluster name not match"
Node_not_exist = "specific node not in cluster"
Vm_not_exist = "vm not in cluster"
Domain_not_exist = "vm domain not exist in libvirt"
Not_primary = "this node is not primary"
Not_backup = "this node is not backup"
Not_node = "this node is not general node"
Ibmp_is_none = "ibmp is none"
Ibmp_is_used = "ibmp is used"
Node_has_exist = "node is in cluster already"
Vm_has_exist = "vm is in cluster already"
Primary_node_not_exist = "can not find primary node in cluster"
Backup_node_not_exist = "can not find backup node in cluster"
Cluster_has_exist = "there is a cluster already exists, you can't create another one"
Already_in_cluster = "this node has already in cluster, you can't create another one"
Not_in_cluster = "this node not in specific cluster"
Node_name_repeat = "this node name is used, please change another one"
Clusterinfo_is_empty = "clusterInfo is empty"
Rmnode_fail_without_backup = "because there is no backup in cluster now, please try again later"
Create_NodeFileFolder_failed = "failed to create node file folder"
Clusterfile_not_json_string = "Cluster file content is not json string"

# vm operation message
Vm_is_running = "the specific vm has run at one of nodes, you cannot start it again"
Vm_not_running = "the specific vm is not running"
Vm_create_success = "create vm by libvirt api successfully"
Vm_create_failed = "failed to create vm by libvirt api"
Vm_destroy_success = "destroy vm by libvirt api successfully"
Vm_destroy_failed = "failed to destroy vm by libvirt api"


# other error messages
Get_ip_address_error = "get wrong self ip"
Socket_timeout_error = "target node does not reply in %s seconds" %(Connect_timeout)

# connect error message
Socket_build_error = "socket build error"
Socket_connect_error = "socket connect error"
Receive_limit = 1024

# the setting of libvirt operation
Libvirt_self_connection = "qemu:///system"

# the return result of libvirt API
Libvirt_return_create_success = 0       # domain.create(), Return 0 in case of success, -1 if error
Libvirt_return_destroy_success = 0      # domain.destroy(), Return 0 in case of success, -1 if error

# the message of libvirt operation
Libvirt_connection_failed = "failed to open connection to %s"
Libvirt_get_domains_failed = "failed to get a list of domain IDs"
Libvirt_create_domain_failed = "failed to create a domain from an XML definition"
Libvirt_create_domain_success = "create a domain from an XML definition successfully"
#StartVM_failed = 'failed to start vm, the state of vm is %s'
Read_xml_file_failed = "failed to read xml file"
CreateVM_exception_message = "failed to create vm"
StartVM_exception_message = "failed to start vm, check the vm name is correct"
ShutdownVM_exception_message = "failed to shutdown vm, check the vm name is correct"
RebootVM_exception_message = "failed to reboot vm, check the vm setting"

# threads name
Thread_command_handler = "CommandHandler"
Thread_vm_manager = "VMManager"
Thread_vm_detector = "VMDetector"
Thread_cluster_maintainer = "ClusterMaintainer"

# event string of VMDetector
Event_string = (
        ( "Added", "Updated" ),
        ( "Removed" ),
        ( "Booted", "Migrated", "Restored", "Snapshot", "Wakeup" ),
        ( "Paused", "Migrated", "IOError", "Watchdog", "Restored", "Snapshot" ),
        ( "Unpaused", "Migrated", "Snapshot" ),
        ( "Shutdown", "Destroyed", "Crashed", "Migrated", "Saved", "Failed", "Snapshot"),
        ( "Finished" )
        )
Event_Crashed = Event_string[5][2]
Event_failed = Event_string[5][5]

# watchdog action list
Event_watchdog_action = (
        libvirt.VIR_DOMAIN_EVENT_WATCHDOG_NONE,         # = 0, No action, watchdog ignored
        libvirt.VIR_DOMAIN_EVENT_WATCHDOG_PAUSE,        # = 1, Guest CPUs are paused
        #libvirt.VIR_DOMAIN_EVENT_WATCHDOG_RESET,       # = 2, Guest CPUs are reset
        libvirt.VIR_DOMAIN_EVENT_WATCHDOG_POWEROFF,     # = 3, Guest is forcibly powered off
        libvirt.VIR_DOMAIN_EVENT_WATCHDOG_SHUTDOWN,     # = 4, Guest is requested to gracefully shutdown
        libvirt.VIR_DOMAIN_EVENT_WATCHDOG_DEBUG,        # = 5, No action, a debug message logged
        libvirt.VIR_DOMAIN_EVENT_WATCHDOG_INJECTNMI,    # = 6, Inject a non-maskable interrupt into guest
        )

# last fail of vm
Lastfail_messages = (
    ( "VMCrashAndRebootSuccess", "vm crashed and has been rebooted now"),
    ( "VMCrashAndRebootFailed", "vm crashed and failed to reboot it" ),
        ( "GuestOSHangAndRebootSuccess", "guest OS hang and has been rebooted now "),
        ( "GuestOSHangAndRebootFailed", "guest OS hang and failed to reboot it")
    )
# max number of trying command times
Max_update_vm_status_times = 2
Max_check_isdir_times = 3

# the format of detection command
Detection_ping_format = "ping -c 1 %s >/dev/null"

# the response of detectin command
Response_ping_success = 0

# the status of node health
Node_status_health = 0
Node_status_hostdown = 1
Node_status_self_network_isolation = 2