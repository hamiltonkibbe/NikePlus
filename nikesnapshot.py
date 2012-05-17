# -*- coding: utf-8 -*-
"""
@file   nikesnapshot.py
@author Hamilton Kibbe
"""

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