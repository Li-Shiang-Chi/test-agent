#!/usr/bin/python
#-*- coding: utf-8 -*-

import os
import sys
import time
import imp
import math
import logging
import data_dir
import cartesian_config
import TA_error
import macro
import postprocess
import shutil

IGNORE_CHAR = ['#', ' ', '\n']
round_log_dir = ""

sys_stdout = sys.stdout
sys_stderr = sys.stderr

pre_error_logger =  None
pro_error_logger =  None
pos_error_logger =  None
pass_logger = None
fail_logger = None

n_tests_total = 0
n_tests_fail = 0
n_tests_pre_error = 0
n_tests_pro_error = 0
n_tests_post_error = 0
n_tests_not_existed = 0

class Bcolors(object):

    """
    Very simple class with color support.
    copied by virttest standalone_test.py
    """

    def __init__(self):
        self.blue = '\033[94m'
        self.green = '\033[92m'
        self.yellow = '\033[93m'
        self.red = '\033[91m'
        self.end = '\033[0m'
        self.HEADER = self.blue
        self.PASS = self.green
        self.SKIP = self.yellow
        self.FAIL = self.red
        self.ERROR = self.red
        self.WARN = self.yellow
        self.ENDC = self.end
        allowed_terms = ['linux', 'xterm', 'xterm-256color', 'vt100',
                         'screen', 'screen-256color']
        term = os.environ.get("TERM")
        if (not os.isatty(1)) or (not term in allowed_terms):
            self.disable()

    def disable(self):
        self.blue = ''
        self.green = ''
        self.yellow = ''
        self.red = ''
        self.end = ''
        self.HEADER = ''
        self.PASS = ''
        self.SKIP = ''
        self.FAIL = ''
        self.ERROR = ''
        self.ENDC = ''

# Instantiate bcolors to be used in the functions below.
bcolors = Bcolors()


class StreamToLogger(object):
  """
  Fake file-like stream object that redirects writes to a logger instance.
  """
  def __init__(self, logger, log_level=logging.INFO):
    self.logger = logger
    self.log_level = log_level
    self.linebuf = ''

  def write(self, buf): #以info的方式寫入，有空格則移至下一行寫入
    for line in buf.rstrip().splitlines():
       self.logger.log(self.log_level, line.rstrip())

  def info(self, string): #以info的方式寫入 寫一行
    self.logger.info(string)

  def error(self, string): #以error的方式寫入 寫一行
    self.logger.error(string)


def extract_macro(parser):
  """
  extract macro form parser
  
  :param parser: is a dict, get from Test config file
  :return mac_ele_list: store all macro element
  """
  mac_ele_list = []
  mac_num = parser["mac_num"]
  if parser["mac_use"] == "all": #抓取出所有被macro納入之參數
    mac_num = int(parser["mac_num"])
    for i in range(1, mac_num+1):
      ele = set_macro_ele(parser, i)
      mac_ele_list.append(ele)
  else:
    """
    assign macro number not all
    僅抓取指定納入之參數
    """
    mac_no_list = parser["mac_use"].split()
    for no in mac_no_list:
      ele = set_macro_ele(parser, int(no))
      mac_ele_list.append(ele)
  return mac_ele_list

def set_macro_ele(parser, ele_no): #把每個macro參數儲存成一個dict
  """
  把每個macro參數儲存成一個dict

  :param parser: is a dict, get from Test config file
  :param ele_no: macro element number
  :return: macro element dict
  """
  return {"mac_no": ele_no
        , "mac_name": parser["mac_"+str(ele_no)]
        , "mac_ori": parser["mac_"+str(ele_no)+"_ori"]
        , "mac_ori_assert": parser["mac_"+str(ele_no)+"_ori_assert"]
        , "lower_bound": int(parser["mac_"+str(ele_no)+"_lower_bound"])
        , "lower_bound_assert": parser["mac_"+str(ele_no)+"_lower_bound_assert"]
        , "upper_bound": int(parser["mac_"+str(ele_no)+"_upper_bound"])
        , "upper_bound_assert": parser["mac_"+str(ele_no)+"_upper_bound_assert"]}


def redirect_stdout(new_stdout):
  """
  redirect stdout

  :param new_stdout: new stdout
  """
  sys.stdout = new_stdout

def restord_stdout():
  """
  return to original stdout
  """
  sys.stdout = sys.__stdout__

def redirect_stderr(new_stderr):
  """
  redirect stderr

  :param new_stderr: new stderr
  """
  sys.stderr = new_stderr

def restord_stderr():
  """
  return to original stderr
  """
  sys.stderr = sys.__stderr__

def redirect_output(new_output):
  """
  redirect stdout stderr

  :param new_output: new stdout stderr
  """
  redirect_stdout(new_output)
  redirect_stderr(new_output)

def restore_output():
  """
  restore stdout stderr
  """
  restord_stdout()
  restord_stderr()


class Test(object):
  def __init__(self, test_info):
    self.test_cfg_path = test_info["test_cfg_dir"]+test_info["test_name"]+".cfg" 
    self.base_cfg_path = data_dir.TESTS_CFG_DIR+"base.cfg"
    self.test_dir = test_info["test_dir"]
    self.test_name = test_info["test_name"]
    self.test_run_name = self.test_name #actually test name ,update when macro feature open
    self.FTlevel = test_info["FTlevel"]
    self.log_dir = os.path.join(round_log_dir, self.test_name+"/")
    self.test_logger = None
    self.parser = {}
    self.flag = 0
    self.macro = test_info["macro"]
    self.macro_ele_list = []
    self.macro_list = [] #use to store each element's value can be changed 
    self.macro_assert = True
    self.macro_no = 0 # use to record what number sequence of macro in this test case

    self.main()

  def __setattr__(self, name, value):
    object.__setattr__(self, name, value)
    #更改assign的method
    #if name == "macro_list":
    #  print self.macro_list
    if name == "macro_list" and self.macro == "open" and self.flag == 1: #若有開啟macro功能且現在被assign的ele為self.macro_list則進入
      #print self.macro_list
      self._macro_list_change()
      self.flag = 0


  def set_macro_list(self, macro_list):
    self.macro_list = macro_list

  def set_flag(self, flag):
    self.flag = flag

  def _set_run_func(self):
    """
    load module from test and get entry run func

    :return run_func: function module
    """
    f, p, d = imp.find_module(self.test_name, [self.test_dir]) #找到test case的module
    test_module = imp.load_module(self.test_name, f, p , d) #載入module
    f.close()
    run_func = getattr(test_module, "run_%s" % self.test_name) #類似c的func pointer的概念，把找到的module存置一個變數中
    return run_func
    

  def _macro_list_change(self):
    """
    when macro list change 
    """
    self.macro_no += 1
    self._update_parser()
    self._update_macro_assert()
    self.update_test_run_name()
    self.run()

  def _update_parser(self):
    """
    update parser by macro_list
    """
    for i in range(0, len(self.macro_ele_list)):
      self.parser[self.macro_ele_list[i]["mac_name"]] = str(self.macro_list[i])

  def _update_macro_assert(self):
    """
    update macro assert result
    """
    self.macro_assert = True
    is_ori = True
    """
    若有任何一個參數改變數值後，會導致測試之結果與原本之數值相反

    則更改數值後測試執行，與未更改數值之測試結果相反視為測試通過

    所以必須設定False為通過，True為不通過
    """
    for i in range(0, len(self.macro_ele_list)):
      if self.macro_list[i] != int(self.macro_ele_list[i]["mac_ori"]):
        is_ori = False
        break
    if not is_ori:
      for i in range(0, len(self.macro_ele_list)):
        if int(self.macro_ele_list[i]["mac_ori"]) > self.macro_list[i]:
          if self.macro_ele_list[i]["lower_bound_assert"] == "False":
            self.macro_assert = False #改成False為測試通過
            break
        else:
          if self.macro_ele_list[i]["upper_bound_assert"] == "False":
            self.macro_assert = False #改成False為測試通過
            break

  def update_test_run_name(self):
    """
    update self.test_run_name
    """
    self.test_run_name = self.test_name + "_" + str(self.macro_no)

  def _parse_test_cfg(self):
    """
    parse test cfg
    """
    try:
      base_parser = cartesian_config.Parser(self.base_cfg_path).get_dicts().next() #把base.cfg的內容存入parser
      test_parser = cartesian_config.Parser(self.test_cfg_path).get_dicts().next() #把test case的.cfg檔內容存入parser
      self.parser = dict(base_parser.items() + test_parser.items()) #合併parser
      #print self.parser
    except Exception, e:
      raise Exception("test case : "+self.test_name+", cfg file problem")

  def create_logger(self):
    """
    create logger for test
    """
    if os.path.exists(self.log_dir):
      f_name = self.test_name
      if self.macro == "open": #若有開啟macro功能 測試案例的記錄檔名稱會在加一個編號 ex: test_1
        f_name = f_name + "_" + str(self.macro_no)
      f_name = f_name + ".log"
      test_log_path = os.path.join(self.log_dir, f_name) #設定記錄檔的路徑
      self.test_logger = logging.getLogger(f_name) #拿到logger 物件
      self.test_logger.setLevel(logging.INFO) 
      self.test_logger.addHandler(logging.FileHandler(test_log_path)) #記錄的內容為寫入檔案不為輸出置螢幕
      self.test_logger = StreamToLogger(self.test_logger, logging.INFO)
      #redirect stdout stderr to logger
      redirect_output(self.test_logger)


  def run(self):
    #run test case
    global n_tests_total
    n_tests_total += 1
    self.create_logger() #創建該測試案例之記錄檔
    #記錄檔寫入測試案例名稱
    self.test_logger.info("test name: "+self.test_name)
    if self.macro == "open": #記錄macro使用之參數
      self.test_logger.info("\nmacro element : ")
      for i in range(0, len(self.macro_ele_list)):
        self.test_logger.info(self.macro_ele_list[i]["mac_name"]+" : "+str(self.macro_list[i]))


    test_pass = False
    try:
      try:
        t_begin = time.time()
        run_func = self._set_run_func()
        #run_func()
        run_func(self.parser) #執行測試案例
        test_pass = True
      finally:
        t_end = time.time()
        t_elapsed = t_end - t_begin #計算該測試案例經過時間
    except TA_error.Assert_Error, e:
      #test case failed
      global n_tests_fail
      global fail_logger
      n_tests_fail += 1
      fail_logger.info(self.test_run_name+"\n") #該測試案例記錄至fail.log
      self.test_logger.info("Fail reason : ")
      self.test_logger.info(e.content)
      if self.macro_assert != False:
        restore_output() #重新導向至輸出螢幕
        print_fail(self.test_run_name, t_elapsed) #資訊輸出至螢幕
        #print e.content
      else:
        test_pass = True
    except TA_error.Preprocess_Error, e:
      #preprocess has some problems
      global n_tests_pre_error
      global pre_error_logger
      n_tests_pre_error += 1
      pre_error_logger.info(self.test_run_name+"\n") #該測試案例記錄至preprocess_error.log
      self.test_logger.info("Preprocess error reason : ")
      self.test_logger.info(e.content)
      restore_output() #重新導向至輸出螢幕
      print_error(self.test_run_name, t_elapsed, "PREPROCESS") #資訊輸出至螢幕
      #print e.content
    except TA_error.Process_Error, e:
      #process has some problems
      global n_tests_pro_error
      global pro_error_logger
      n_tests_pro_error += 1
      pro_error_logger.info(self.test_run_name+"\n") #該測試案例記錄至process_error.log
      self.test_logger.info("Process error reason : ")
      self.test_logger.info(e.content)
      restore_output() #重新導向至輸出螢幕
      print_error(self.test_run_name,t_elapsed, "PROCESS") #資訊輸出至螢幕
      #print e.content
    except Exception, e:
        print e.content
        self.test_logger.info(str(e))
    finally:
      try:
        if test_pass == True:

          global pass_logger
          pass_logger.info(self.test_run_name+"\n")
          restore_output()
          print_pass(self.test_run_name,t_elapsed)
          redirect_output(self.test_logger)
       # postprocess.postprocess(self.parser)
      except TA_error.Postprocess_Error, e:
        #print "postprocess error"
        global n_tests_post_error
        global pos_error_logger
        n_tests_post_error += 1
        pos_error_logger.info(self.test_run_name+"\n") #該測試案例記錄至postprocess_error.log
        self.test_logger.info("Postprocess error reason : ")
        self.test_logger.info(e.content)
        restore_output() #重新導向至輸出螢幕
        print_error(self.test_run_name,t_elapsed, "POSTPROCESS") #資訊輸出制螢幕
        #print e.content
      finally:
        restore_output()
    #copy log file for further use
    #shutil.copyfile("/var/log/libvirt/libvirtd.log", self.log_dir + "libvirt_" + str(self.macro_no) + ".log")
    

  def main(self):
    self._parse_test_cfg()  #parse test cfg file
    if self.macro == "open":
      #print "open"
      self.macro_ele_list = extract_macro(self.parser)
      macro.new_macro(self.macro_ele_list,self)
    else:
      """
      no macro, only run once
      """
      self.run()

def transfer_co_to_tests_list(f_name, tests_list):
  """
  transfer *.co content to tests_list

  :param f_name: file name
  :param tests_list: store all test cases info
  """
  f = open(os.path.join(data_dir.COMBINATION_TESTS_DIR, f_name+".co"),'r') #開啟.co檔
  line = f.readline().rstrip('\n')
  file_type = ""
  test_dir = ""
  test_cfg_dir = ""
  macro_type = "close"
  while line:
    """
    逐行讀取分析.co檔
    """
    if line == "!co":
      file_type = "co"
    elif line == "!0":
      file_type = '0'
      test_dir = data_dir.GENERAL_TESTS_DIR
      test_cfg_dir = data_dir.GENERAL_TESTS_CFG_DIR
    elif line == "!1":
      file_type = '1'
      test_dir = data_dir.L1_TESTS_DIR
      test_cfg_dir = data_dir.L1_TESTS_CFG_DIR
    elif line == "!2":
      file_type = '2'
      test_dir = data_dir.L2_TESTS_DIR
      test_cfg_dir = data_dir.L2_TESTS_CFG_DIR
    elif line == "!3":
      file_type ='3'
      test_dir = data_dir.L3_TESTS_DIR
      test_cfg_dir = data_dir.L3_TESTS_CFG_DIR
    elif line == "!m":
      macro_type = "open"
    elif line == "!m!":
      macro_type = "close"
    else:
      if not line[0] in IGNORE_CHAR:
        if file_type == "co": #若是co檔，則繼續往下分析
          transfer_co_to_tests_list(line, tests_list) 
        else: #儲存測試案例資訊：測試案例名稱 測試案例所在資料夾 測試案例設定擋資料夾 測試案例檔案分類 是否開啟macro
          tests_list.append(
            set_test_dict(
            line, test_dir, test_cfg_dir, file_type, macro_type))
    line = f.readline().rstrip('\n')

def set_test_dict(test_name, test_dir, test_cfg_dir, FTlevel, macro = "close"):
  """
  set test dict
  macro :default is "close"
  """
  #print macro
  return {"test_name": test_name, "test_dir": test_dir
    , "test_cfg_dir": test_cfg_dir, "FTlevel": FTlevel, "macro": macro}


def set_tests_list(options):
  """
  set all tests in tests_list in this round

  :param options: run FTVMTA command option

  """
  tests_list = []
  if options.comb != None:
    """
    multiple test cases
	
    交由transfer_co_to_tests_list作處理
    """
    transfer_co_to_tests_list(options.comb, tests_list)
  if options.comb == None and options.FTlevel != None:
    """
    only one test case
	
    #儲存測試案例資訊：測試案例名稱 測試案例所在資料夾 測試案例設定擋資料夾 測試案例檔案分類 是否開啟macro
    """
    test = {}
    if options.FTlevel == '0':
      test = set_test_dict(options.test, data_dir.GENERAL_TESTS_DIR
        ,data_dir.GENERAL_TESTS_CFG_DIR,options.FTlevel)
    if options.FTlevel == '1':
      test = set_test_dict(options.test, data_dir.L1_TESTS_DIR
        , data_dir.L1_TESTS_CFG_DIR, options.FTlevel)
    if options.FTlevel == '2':
      test = set_test_dict(options.test, data_dir.L2_TESTS_DIR
        , data_dir.L2_TESTS_CFG_DIR, options.FTlevel)
    if options.FTlevel == '3':
        test = set_test_dict(options.test , data_dir.L3_TESTS_DIR , data_dir.L3_TESTS_CFG_DIR , options.FTlevel)
    tests_list.append(test)
  return tests_list

def check_test_exist(test):
  """
  check test exist or not
  
  :return: true/false
  """
  
  for f in os.listdir(test["test_dir"]):
    if f.endswith(".py") and (f == test["test_name"]+".py"):
      return True
  return False

def create_round_log_dir():
  """
  create log dir for round test
  """
  global round_log_dir
  tests_start_time = time.strftime('%Y-%m-%d-%H.%M.%S')
  print "\nTests at "+tests_start_time+"\n"
  log_dir_name = tests_start_time+"/"
  round_log_dir = os.path.join(data_dir.LOG_DIR, log_dir_name)
  if not os.path.exists(round_log_dir):
    os.makedirs(round_log_dir)

def create_test_log_dir(test_name):
  """
  create log dir for test
  """
  global round_log_dir
  if os.path.exists(round_log_dir):
    test_dir_name = test_name + "/"
    test_log_dir = os.path.join(round_log_dir, test_dir_name)
    if not os.path.exists(test_log_dir):
      os.makedirs(test_log_dir)

def create_round_log_files():
  """
  create file about this round test
  """
  global round_log_dir
  global pre_error_logger
  global pro_error_logger
  global pos_error_logger
  global pass_logger
  global fail_logger
  if os.path.exists(round_log_dir):
    #設定preprocess_error.log
    pre_error_file_path = os.path.join(round_log_dir, "preprocess_error.log")
    pre_error_logger = logging.getLogger("pre_error")
    pre_error_logger.setLevel(logging.INFO) 
    pre_error_logger.addHandler(logging.FileHandler(pre_error_file_path))
	
    #設定process_error.log
    pro_error_file_path = os.path.join(round_log_dir, "process_error.log")
    pro_error_logger = logging.getLogger("pro_error")
    pro_error_logger.setLevel(logging.INFO) 
    pro_error_logger.addHandler(logging.FileHandler(pro_error_file_path))
	
    #設定postprocess_error.log
    pos_error_file_path = os.path.join(round_log_dir, "postprocess_error.log")
    pos_error_logger = logging.getLogger("pos_error")
    pos_error_logger.setLevel(logging.INFO) 
    pos_error_logger.addHandler(logging.FileHandler(pos_error_file_path))
	
    #設定fail.log
    fail_file_path = os.path.join(round_log_dir, "fail.log")
    fail_logger = logging.getLogger("fail")
    fail_logger.setLevel(logging.INFO) 
    fail_logger.addHandler(logging.FileHandler(fail_file_path))
	
    #設定pass.log
    pass_file_path = os.path.join(round_log_dir, "pass.log")
    pass_logger = logging.getLogger("pass")
    pass_logger.setLevel(logging.INFO) 
    pass_logger.addHandler(logging.FileHandler(pass_file_path))
    #pass_logger.error('1')
    #print logging.Logger.manager.loggerDict.keys()



def print_pass(test_name, time):
  print(test_name+" "+bcolors.PASS + "PASS" +
                 bcolors.ENDC + " (%.2f s)" % time)

def print_fail(test_name, time):
  print(test_name+" "+bcolors.FAIL + "FAIL" +
                 bcolors.ENDC + " (%.2f s)" % time)

def print_error(test_name, time, err_type):
  print(test_name+" "+bcolors.ERROR +err_type+" ERROR" +
                 bcolors.ENDC + " (%.2f s)" % time)

def print_result():
  """
  print the final result of round test
  
  輸出最後測試之結果至螢幕
  """
  global n_tests_total
  global n_tests_fail
  global n_tests_pre_error
  global n_tests_pro_error
  global n_tests_post_error
  global n_tests_not_existed
  n_tests_pass = n_tests_total - n_tests_pre_error - n_tests_pro_error - n_tests_fail
  success_rate = (float(n_tests_pass) / float(n_tests_total)) * 100
  print "--------------------------------------------------------"
  if n_tests_not_existed != 0:
    print (bcolors.SKIP+"Test case not existed" + bcolors.ENDC + " : %d" % n_tests_not_existed)
  print (bcolors.FAIL+"Preprocess error" + bcolors.ENDC + " : %d" % n_tests_pre_error)
  print (bcolors.FAIL+"Process error" + bcolors.ENDC + " : %d" % n_tests_pro_error)
  print (bcolors.FAIL+"Postprocess error" + bcolors.ENDC + " : %d" % n_tests_post_error)
  print (bcolors.FAIL+"Fail" + bcolors.ENDC + "/"
        + bcolors.HEADER+"Total" + bcolors.ENDC 
        + " : %d/%d" % (n_tests_fail, n_tests_total))
  print (bcolors.PASS+"Pass" + bcolors.ENDC + "/"
        + bcolors.HEADER+"Total" + bcolors.ENDC 
        + " : %d/%d" % (n_tests_pass, n_tests_total))
  print (bcolors.HEADER+"Success rate:" + bcolors.ENDC + " : %.2f %%" % success_rate)

def run_tests(options):
  """
  accroding to tests_list to run all tests
  """

  global n_tests_not_existed
  create_round_log_dir()
  create_round_log_files()
  test_lists = set_tests_list(options)
  for test in test_lists: #逐個進行測試案例
    if check_test_exist(test):
      create_test_log_dir(test["test_name"])
      t = Test(test)
    else:
      n_tests_not_existed += 1
  global n_tests_total
  if n_tests_total > 0:
    print_result()





if __name__ == "__main__":
  parser = cartesian_config.Parser("../tests/L1_tests/cfg/test1.cfg").get_dicts().next()
  mac_ele_list = extract_macro(parser)
  #print mac_ele_list
  macro.macro(mac_ele_list)




