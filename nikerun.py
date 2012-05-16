# -*- coding: utf-8 -*-

from xml.etree import ElementTree as xmlTree

class NikeRunStats:
    """
    Class for storing information about a run
    """
    
    def __init__(self,xmlRun):
        """
        Create a run instance from Nike+ API XML data
        """
        self._id = xmlRun.get('id')
        self._distance = float(xmlRun.find('distance').text)
        self._duration = int(xmlRun.find('duration').text)
        self._hours = self._duration / 3600000
        self._minutes = self._duration % 360000 / 60000
        self._seconds = self._duration % 3600000 % 60000 / 1000
        self._date = 0
        self._time = 0
        self._calories = float(xmlRun.find('calories').text) 
        
    @property   
    def RunId(self):
        """
        Return the run ID as a string
        """
        
        return str(self._id)        
        
        
    @property 
    def DistanceKilometers(self):
        """ 
        Return the run distance in kilometers
        """
        
        return ('%.2f' % self._distance)
    
    
    @property
    def DistanceMiles(self):
        """ 
        Return the run distance in miles
        """
        
        return ("%.2f" % (self._distance * 0.621371192))
        
   
    @property
    def Duration(self):
        """
        Return the run duration in the form HH:MM:SS
        """  
        
        return  ('%02d' % self._hours) + ':' + ('%02d' % self._minutes) + ':' + ('%02d' % self._seconds)


    @property
    def Calories(self):
        """
        Return the number of calories burned
        """
        
        return self._calories




class NikeSnapshotList:
    def __init__(self,xmlSnapshotList):
        self.type = xmlSnapshotList.get('snapShotType')
        self.snapshots = [NikeSnapshot(snapshot) for snapshot in xmlSnapshotList.findall('snapShot')]



class NikeSnapshot:
    def __init__(self,xmlSnapshot):
        self._id = xmlSnapshot.get('id')
        self.event = xmlSnapshot.get('event')
        self.pace = xmlSnapshot.find('pace').text
        self.distance = xmlSnapshot.find('distance').text
        self.duration = xmlSnapshot.find('duration').text

      

class NikeRun:

    def __init__(self, xmlRun):
        
        if xmlRun.find('status').text != 'success':
            print "Error. Could not get run data"
            return 0
            
        sportsData = xmlRun.find('sportsData')
        runSummary = sportsData.find('runSummary')
        extendedDataList = sportsData.find('extendedDataList')
        
        # Run Summary
        self.startTime = sportsData.find('startTime').text
        self.distance = float(runSummary.find('distance').text)
        self.duration = int(runSummary.find('duration').text)
        self.calories = float(runSummary.find('calories').text)
        self.snapshotLists = [NikeSnapshotList(sslist) for sslist in sportsData.findall('snapShotList')]
        
        # Run Distance
        self.extendedDistanceInterval = int(extendedDataList.find('extendedData').get('intervalValue'))
        self.extendedDistanceList = [float(data) for data in extendedDataList.find('extendedData').text.split(',')]
        self.speedList = [(3600/self.extendedDistanceInterval) * dist for dist in  self.extendedDistanceList]
        
        # Run Metadata
        self.hasHRS = runSummary.get('hasHRS')
        self.workoutType = runSummary.get('workoutType')
        self.equipmentType = runSummary.find('equipmentType').text
        self.howFelt = int(sportsData.find('howFelt').text)
        self.weather = int(sportsData.find('weather').text)
        self.terrain = int(sportsData.find('terrain').text)
        print self.speedList[0]
    