# -*- coding: utf-8 -*-
"""
@file   nikegps.py
@author Hamilton Kibbe

"""
import json
from xml.etree.ElementTree import TreeBuilder

class NikeGPS(object):
	def __init__(jsonGps):
		gps = json.load(jsonGps)
		
		
	def getGPX():
		

		gpx = TreeBuilder()		
		gpx.start('gpx',{'version':				'1.2',
						 'creator':				'NikePlus',
						 'xmlns:xsi':			'http://www.w3.org/2001/XMLSchema-instance',
						 'xmlns':				'http://www.topografix.com/GPX/1/2/',
						 'xsi:schemaLocation': 	'http://www.topografix.com/gpx/1/2/gpx.xsd'})
		
		gpx.start('metadata',{})
		gps.start('name',{})