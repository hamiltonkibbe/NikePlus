# -*- coding: utf-8 -*-
"""
@file   nikeurls.py
@author Hamilton Kibbe
"""
import urllib2

class NikeURLs(object):
    def __init__(self):
        self._BASE_URL = "https://secure-nikerunning.nike.com/nikeplus/v2/services/app/"
        self._AUTH_URL = self._BASE_URL+"generate_pin.jsp?"
        self._RUNLIST_URL = self._BASE_URL+"run_list.jsp"
        self._RUNDATA_URL = self._BASE_URL+"get_run.jsp?"
        self._GPS_URL = self._BASE_URL+"get_gps_detail.jsp?"
	
    def authURL(self,username,password):
        return self._AUTH_URL+'login='+urllib2.quote(username)+'&password='+urllib2.quote(password)

    def runURL(self,runId):
        return self._RUNDATA_URL+'id='+str(runId)
    
    def gpsURL(self,runId):
        return self._GPS_URL+'id='+str(runId)

