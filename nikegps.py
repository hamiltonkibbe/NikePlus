# -*- coding: utf-8 -*-
"""
@file   nikegps.py
@author Hamilton Kibbe

"""
import json
from datetime import datetime
from xml.etree.ElementTree import ElementTree, TreeBuilder



class NikeTrackPoint:
	"""
	Waypoint class used in creating GPX file
	"""
	
	def __init__(self,jsonTrackPoint):
		self._lat = float(jsonTrackPoint['lat'])
		self._lon = float(jsonTrackPoint['lon'])
		self._alt = float(jsonTrackPoint['alt'])
		self._time = int(jsonTrackPoint['time'])
	
	@property
	def latLon(self):
		return [self._lat,self._lon]
		
	@property
	def lat(self):
		return self._lat
	
	@property
	def lon(self):
		return self._lon
	
	@property
	def altitudeMeters(self):
		return self._alt

	@property
	def altitudeFeet(self):
		return self._alt * 3.2808399
	
	@property
	def time(self):
		return datetime.utcfromtimestamp(self._time/1000)




class NikeGPS(object):
	"""
	Stores Nike+ GPS data and exports to GPX
	"""
	
	def __init__(self,jsonGps):
		gps = jsonGps['plusService']
		gpsRoute = gps['route']
		gpsData = gps['sportsData']
		
		self._runId = gpsData['id']
		self._date = gpsData['route']['name'].split(',')[0]
		self._startTime = gpsData['route']['name'].split(',')[1]
		self._trackPointList = [NikeTrackPoint(trkpt) for trkpt in gpsRoute['waypointList']]
	
	@property
	def waypoints(self):
		return self._trackPointList
	
	
	def getGPX(self,fileName):
		
		gpx = TreeBuilder()
		
		# GPX tag
		gpx.start('gpx',{'version':				'1.2',
						 'creator':				'NikePlus',
						 'xmlns:xsi':			'http://www.w3.org/2001/XMLSchema-instance',
						 'xmlns':				'http://www.topografix.com/GPX/1/2/',
						 'xsi:schemaLocation': 	'http://www.topografix.com/GPX/1/2/ http://www.topografix.com/gpx/1/2/gpx.xsd'})
		
		# Metadata
		gpx.start('metadata',{})
		# Meta Name
		gpx.start('name',{})
		gpx.data('Run ' + self._runId)
		gpx.end('name')
		
		#Bounds
		minLat = min([point.lat for point in self._trackPointList])
		maxLat = max([point.lat for point in self._trackPointList])
		minLon = min([point.lon for point in self._trackPointList])
		maxLon = max([point.lon for point in self._trackPointList])
		extents = {'minLat':str(minLat), 'maxLat':str(maxLat),'minLon':str(minLon),'maxLon':str(maxLon)}
		gpx.start('bounds',extents)
		gpx.end('bounds')
		
		# Metadata close
		gpx.end('metadata')
		
		# Track
		gpx.start('trk',{})
		
		# Track Name
		gpx.start('name',{})
		gpx.data(str(self._runId))
		gpx.end('name')	
		
		# Track Type
		gpx.start('type',{})
		gpx.data('Run')
		gpx.end('type')
		
		gpx.start('trkseg',{})
		
		for point in self._trackPointList:
			
			gpx.start('trkpt',{'lat':str(point.lat),'lon':str(point.lon)})
			
			gpx.start('ele',{})
			gpx.data(str(point.altitudeMeters))
			gpx.end('ele')
			
			gpx.start('time',{})
			gpx.data(point.time.strftime('%Y-%m-%dT%H:%M:%SZ'))	
			gpx.end('time')
			
			gpx.end('trkpt')
		
		gpx.end('trkseg')
		
		gpx.end('trk')
		
		gpx.end('gpx')
		
		gpxFile = ElementTree(gpx.close())
		
		gpxFile.write(open(fileName,'wb'),'utf-8')
		
		
		