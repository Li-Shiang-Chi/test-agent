#!/usr/bin/python
#-*- coding: utf-8 -*-
'''
@author: lsc

this is a class which represent the HA3.0 terminal message
'''

# error message
Nfs_folder_not_exist = "nfs file doesn't exist or is empty"
Mounting_folder_not_exist = "nfs mounting folder dosen't exist"
Nfs_file_content_error = "can not found nfs ip or mounting folder path in nfs file"
Get_ip_address_error = "get wrong self ip"
Node_file_not_exist = "node file doesn't exist or is empty"
Cluster_file_not_exist = "cluster file doesn't exist or is empty"
Cluster_name_not_match = "cluster name not match"
Node_not_exist = "specific node not in cluster"
Vm_not_exist = "vm not in cluster"
Not_primary = "this node is not primary"
Ibmp_is_none = "ibmp is none"
Ibmp_is_used = "ibmp is used"
Node_has_exist = "node is in cluster already"
Vm_has_exist = "vm is in cluster already"
Primary_node_not_exist = "can not find primary node in cluster"
Cluster_has_exist = "there is a cluster already exists, you can't create another one"
Already_in_cluster = "this node has already in cluster, you can't create another one"
Create_cluster_success = "create cluster success"
Decluster_success = "decluster success"
Add_node_success = "add node success"
Not_in_cluster = "this node not in specific cluster"
Node_name_repeat = "this node name is used, please change another one"
overview = ">> cluster_name: test_c"+ "\n" + "  node name: test_n  role: primary  node_ip: 192.168.44.132  last_fail: None" + "\n"+">>"
