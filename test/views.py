# coding: utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from log import Log 
def test(request, test):
    print "service.....doing test="+test
    d="{service:the details are in the log..... }"
    Log.log('i am the msg')
    Log.log('logInfo',Log.ERROR)
    return HttpResponse(json.dumps(d), mimetype="application/json")

