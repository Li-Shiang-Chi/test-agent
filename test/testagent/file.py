#!/usr/bin/python
#-*- coding: utf-8 -*-

'''

@author: lsc
'''

import os

"""
delete file in specific path
input :(String) path : file path
output :(boolean) success or not
"""

def delete_file(path) :
    if( if_file_exists(path) ) :
        os.remove(path)
        return True
    else:
        print("file %s not exist"  % path)
        return False

"""
reset file content in specific path
input :(String) path : file path
output :(boolean) None
"""

def reset_file(path) :
    if( if_file_exists(path) ):
        f = open(path , "w")
        f.close()
    else:
        open(path , "w").close() #if not found file , create a empty file

"""
get file content(String) in specific path
input :(String) path : file path
output :(String) file content
       (boolean) False , file not found
"""
def get_file_content (path , ssh = None) :
    if ssh:
            return get_remote_file_content(path, ssh)
    else:
        if( if_file_exists(path) ) :
            f = open(path , 'r')
            return f.read()
        else:
            return False
"""
get remote file content(String) in specific path
input :(String) path : file path
       (ssh) ssh : shell server
output :(String) file content
"""
def get_remote_file_content(path , ssh):
    cmd = "cat %s" % path
    s_stdin, s_stdout, s_stderr = ssh.exec_command(cmd)
    return s_stdout.read()
"""
check file is existing
input :(String) path : file path
output : (boolean) file is existing or not

"""
    
def if_file_exists(path) :
    if(os.path.exists(path)):
        return True
    else:
        return False
"""
Convert relevant path to abs path
input :(String) path : file path
output : (String) absolute path

"""    
def abs_path(relpath):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    path_name = os.path.join(base_dir , relpath)
    if (relpath == None): return os.path.abspath(base_dir)
    return os.path.abspath(path_name)


