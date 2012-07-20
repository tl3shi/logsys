LOG_PATH='/home/tanglei/log/'

#log const
TIME = 'time'
PID = 'pid'
TYPE = 'type'
REQUEST_ID = 'requestid'
CONTENT = 'content'
PARAM='param'
URL = 'url'
PROC_TIME = 'proc_time'
UA = 'user-agent'
STATUS = 'status'
REMOTEIP='remote_ip'
LOG_REQUEST = 'request'
LOG_RESPONSE = 'response'
LOG_DEBUG = 'debug'


LOG_FORMAT='%(asctime)s - %(levelname)s - %(message)s'

#if set to True,the request unique id and the process dealing time will be log,BUT the request.path is changed longer, be attention(maybe,u can use request.path_info to get the original url).
LOG_PROC_INFO = True
# if set to True, the response content may be too much long.
LOG_RESPONSE_HTML=False 
