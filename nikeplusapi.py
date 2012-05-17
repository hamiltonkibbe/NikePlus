# -*- coding: utf-8 -*-

from nikeurls import NikeURLs
from nikerun import NikeRun, NikeRunStats

import urllib2, cookielib
from xml.etree import ElementTree as xmlTree



class NikePlusAPI:
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
        
        if xml.find("status").text != "success":
            print "Failed to authenticate."
            return
        
        self._PIN = xml.find("pin").text

    def getRunList(self):
        runList = xmlTree.fromstring(urllib2.urlopen(self.URLs._RUNLIST_URL).read())
        self.RunList = [NikeRunStats(run) for run in runList.find('runList').findall('run')]
	return self.RunList        
    
    def getRun(self,id):
	xmlRun = xmlTree.fromstring(urllib2.urlopen(self.URLs.runURL(id)).read())
	return NikeRun(xmlRun)	    



SYNC = NikePlusAPI("hamilton.kibbe@gmail.com","silvermine")
runs = SYNC.getRunList()
SYNC.getRun(str(runs[0].RunId))
