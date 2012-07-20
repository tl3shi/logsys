# coding: utf-8
from common.db import DBUtil
import common.constants as CT
import common.util as CU
import copy

def ping(ak, ip, udid):
    dt      = CU.millis()
    pingqr  = {CT.APPKEY: ak, CT.IP: ip, CT.DT: dt}
    pingup  = copy.copy(pingqr)
    pingup[CT.STATUS] = CT.STANEW
    if udid != None:
        pingup[CT.UDID] = udid

    userqr  = {CT.APPKEY: ak, CT.IP: ip}
    userup  = copy.copy(pingqr)
    if udid != None:
        userup[CT.UDID] = udid
 
    DBUtil.findandmodify(CT.COL_PING, _query = pingqr, _update = pingup, _upsert = True)
    DBUtil.findandmodify(CT.COL_USER, _query = userqr, _update = userup, _upsert = True)
    return {CT.STATUS: 1}
