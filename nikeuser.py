# -*- coding: utf-8 -*-
"""
@file   nikeuser.py
@author Hamilton Kibbe

"""

class NikeUser(object):
    def __init__(self,xmlUser):
        self._weight = float(xmlUser.find('weight').text)
        self._device = xmlUser.find('device').text
        
        
    @property 
    def weightKg(self):
        return '%0.1f' % self._weight
        
    @property
    def weightLbs(self):
        return '%0.1f' % (self._weight * 2.20462262)
    
    @property
    def device(self):
        return self._device