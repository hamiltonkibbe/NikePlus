# -*- coding: utf-8 -*-

from xml.etree import ElementTree as xmlTree


class NikeUser(object):
    def __init__(self,xmlUser)
        self._weight = xmlUser.find('weight').text
        self._equipmentType = xmlUser.find('equipmentType').text
        
    @property 
    def weightKg(self):
        return '%0.1f' % self._weight
        
    @property
    def weightLbs(self):
        return '%0.1f' % (self._weight * 2.20462262)
        
    



class NikeRunStats(object):
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




class NikeSnapshotList(object):
    def __init__(self,xmlSnapshotList):
        self._type = xmlSnapshotList.get('snapShotType')
        self._KmSnapshots = [NikeSnapshot(snapshot) for snapshot in xmlSnapshotList.findall('snapShot')]
        
        
    @property
    def type(self):
        return self._type



class NikeSnapshot(object):
    def __init__(self,xmlSnapshot):
        self._id = xmlSnapshot.get('id')
        self.event = xmlSnapshot.get('event')
        self.pace = xmlSnapshot.find('pace').text
        self.distance = xmlSnapshot.find('distance').text
        self.duration = xmlSnapshot.find('duration').text

      

class NikeRun(object):

    def __init__(self, xmlRun):
        
        if xmlRun.find('status').text != 'success':
            print "Error. Could not get run data"
            return 0
            
        sportsData = xmlRun.find('sportsData')
        userInfo = sportsData.find('userInfo')
        runSummary = sportsData.find('runSummary')
        extendedDataList = sportsData.find('extendedDataList')
        self._user = NikeUser(userInfo)
        
        # Run Summary
        self._startTime = sportsData.find('startTime').text
        self._distance = float(runSummary.find('distance').text)
        self._duration = int(runSummary.find('duration').text)
        self._hours = self._duration / 3600000
        self._minutes = self._duration % 360000 / 60000
        self._seconds = self._duration % 3600000 % 60000 / 1000
        self._calories = float(runSummary.find('calories').text)
        
        # Distnace / Split / Pace data
        self._snapshotLists = [NikeSnapshotList(sslist) for sslist in sportsData.findall('snapShotList')]
        self._extendedDistanceInterval = int(extendedDataList.find('extendedData').get('intervalValue'))
        self._extendedDistanceList = [float(data) for data in extendedDataList.find('extendedData').text.split(',')]
        self._speedList = [(3600/self.extendedDistanceInterval) * dist for dist in  self.extendedDistanceList]
        
        # Run Metadata
        self._hasHRS = runSummary.get('hasHRS')
        self._workoutType = runSummary.get('workoutType')
        self._equipmentType = runSummary.find('equipmentType').text
        self._howFelt = int(sportsData.find('howFelt').text)
        self._weather = int(sportsData.find('weather').text)
        self._terrain = int(sportsData.find('terrain').text)

    def KmSplitSnapshots(self):
        for sslist in self._snapshotLists:
            if sslist._type = 'kmSplit':
                theSnapshotList = sslist
        return [snapshot for snapshot in theSnapshotList]
    
    def MileSplitSnapshots(self):
        for sslist in self._snapshotLists:
            if sslist._type = 'mileSplit':
                theSnapshotList = sslist
        return [snapshot for snapshot in theSnapshotList]
        
    def UserClickSnapshots(self):
        for sslist in self._snapshotLists:
            if sslist._type = 'userClick':
                theSnapshotList = sslist
        return [snapshot for snapshot in theSnapshotList]    
        
    @property
    def startTime(self):
        """
        Need to convert this wacky string to something more meaningful
        """
        return self._startTime
    
    @property
    def distanceKilometers(self):
        return '%0.2f' % self._distance
    
    @property
    def distanceMiles(self):
        return '%0.2f' % (self._distance * 0.621371192)
        
    @property
    def duration(self):
        return  ('%02d' % self._hours) + ':' + ('%02d' % self._minutes) + ':' + ('%02d' % self._seconds)
        
    @property
    def calories(self):
        return '%0.1f' % self._calories
    
    @property
    def howFelt(self):
        howFelt = ['Awesome', 'So-so', 'Sluggish', 'Injured']
        return howFelt[(self._howFelt - 1)]
        
    @property
    def weather(self):
        weather = ['Sunny', 'Cloudy', 'Rainy', 'Snowy']
        return weather[(self._weather - 1)]
        
    @property
    def terrain(self):
        terrain = ['Road', 'Trail', 'Treadmill', 'Track']
        return terrain[(self._terrain -1)]
        
    