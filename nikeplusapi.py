# -*- coding: utf-8 -*-
"""
@file   nikeplusapi.py
@author Hamilton Kibbe
"""
from nikeurls import NikeURLs
from nikerun import NikeRun, NikeRunStats
from nikegps import NikeGPS

import urllib2, cookielib
import json
from xml.etree import ElementTree as xmlTree



class NikePlusAPI(object):
    def __init__(self,username,password):
        self.URLs = NikeURLs()
        self.username = username
        self.password = password
        self.authenticate()
    
    def authenticate(self):
        
        self.CJ = cookielib.CookieJar()
        handler = urllib2.HTTPCookieProcessor(self.CJ)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)
        
        xmlResponse = urllib2.urlopen(self.URLs.authURL(self.username,self.password))
        xml = xmlTree.fromstring(xmlResponse.read())

        if xml is None:
            print'Failed to connect'
            return None

        if xml.find('status') is None or xml.find('status').text != 'success':
            print'Authentication failed.'
            return None
   
        self._PIN = xml.find('pin').text


    def getRunList(self):
        runList = xmlTree.fromstring(urllib2.urlopen(self.URLs._RUNLIST_URL).read())
        self.RunList = [NikeRunStats(run) for run in runList.find('runList').findall('run')]
        return self.RunList 
    
    def getRun(self,runId):
        xmlRun = xmlTree.fromstring(urllib2.urlopen(self.URLs.runURL(runId)).read())
        return NikeRun(xmlRun)	    

    def getGps(self,runId):
        jsonGPS = json.loads(urllib2.urlopen(self.URLs.gpsURL(runId)).read())
        return NikeGPS(jsonGPS)


