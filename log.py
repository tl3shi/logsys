import time
import os
import hashlib
import logging
import logconfig 
from os import path

base_dir = logconfig.LOG_PATH
log_path = base_dir + "/" + time.strftime('%Y/%m/',time.localtime(time.time()))
if not os.path.exists(log_path):
    os.makedirs(log_path)

class Log:
   
    today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    logger_dic = {logconfig.LOG_REQUEST:None, logconfig.LOG_RESPONSE:None,logconfig.LOG_DEBUG:None,}
    DEBUG = logging.DEBUG
    ERROR = logging.ERROR
    INFO = logging.INFO
    WARNING = logging.WARNING

    @classmethod
    def init_logger(cls, _today, _type):
        logger = logging.getLogger(_today+_type)
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(log_path+_today+'.'+_type)
        fh.setLevel(logging.INFO)
        if logconfig.LOG_FORMAT != None:
            formatter = logging.Formatter(logconfig.LOG_FORMAT)
        else:
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        cls.logger_dic[_type] = logger

    @classmethod
    def get_logger(cls, _today, _type):
        if (cls.today == _today) and (cls.logger_dic[_type] != None):
            pass
        else:
            Log.init_logger(_today, _type)
            cls.today = _today
        return cls.logger_dic[_type]
    
    @classmethod
    def log(cls, msg, level=logging.INFO):
        _today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        _time = cls.millis()
        _pid = os.getpid()
        content = {
                logconfig.TIME:_time, 
                logconfig.PID:_pid, 
                logconfig.CONTENT:msg,
                #'line':sys._getframe().f_back.f_lineno_
                 }
        log_content = str(content)
        Log.get_logger(_today,logconfig.LOG_DEBUG).log(level,log_content)
   
    @classmethod
    def millis(cls):
        return int(round(time.time() * 1000))
    
    @classmethod
    def log_request(cls,request):
        _today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        _type = request.method
        _url = request.build_absolute_uri()
        _time = Log.millis()
        _pid = os.getpid()
        _content = {}
        _ua = request.META['HTTP_USER_AGENT']
        _remoteIP = request.META['REMOTE_ADDR']

        if _type == 'POST':
            #_content = str(request.POST)
             for k in request.POST.keys():
                _content[k] = request.POST[k]
        else:
           # _content = str(request.GET)
            for k in request.GET.keys():
                _content[k] = request.GET[k]
        _m = hashlib.md5()
        dt = time.time()
        rawid   = str(dt) + '-' + str(_content)
        _m.update(rawid) 
        _request_id = _m.hexdigest()
        log_content = {
                logconfig.TIME : _time,
                logconfig.PID : _pid,
                logconfig.PARAM : _content,
                logconfig.UA : _ua,
                logconfig.REQUEST_ID : _request_id,
                logconfig.TYPE : _type,
                logconfig.URL : _url,
                logconfig.REMOTEIP : _remoteIP
                }
        Log.get_logger(_today,logconfig.LOG_REQUEST).info(str(log_content))
        if logconfig.LOG_PROC_INFO == True:
            request.path = request.path+'?umeng_proc_start_time='+str(_time)+'&umeng_request_id='+str(_request_id)

    @classmethod
    def log_response(cls,request,response):
        
        _today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        _time = Log.millis()
        _pid = os.getpid()
        
        if logconfig.LOG_PROC_INFO == True:
            temp= (request.path.split("?umeng_proc_start_time=")[1]).split('&umeng_request_id=')
            _proc_start_time = int(temp[0])
            _request_id = temp[1]
            _proc_time = _time - _proc_start_time
        
        content = str(response)

        if response.get('Content-Type') == 'text/html' :
            if logconfig.LOG_RESPONSE_HTML == True:
                pass
            else:
                content = 'Content-Type is text/html,the function log html is closed in the Logconfig'
        
        log_content = {
                logconfig.TIME:_time, 
                logconfig.PID:_pid, 
                logconfig.STATUS:response.status_code,
                logconfig.URL:request.path_info,
                logconfig.CONTENT:content,
                }
        print request.path_info

        if logconfig.LOG_PROC_INFO == True:
            log_content[logconfig.REQUEST_ID] = _request_id
            log_content[logconfig.PROC_TIME] = _proc_time
        log_content = str(log_content) 
        Log.get_logger(_today,logconfig.LOG_RESPONSE).info(log_content)

