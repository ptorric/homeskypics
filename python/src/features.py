# -*- coding: utf-8 -*-
"""
homeskypics
Copyright (C) 2019 the homeskypics team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
from matplotlib import pyplot as plt
from aPoint import APoint
import numpy as np
import cv2
from imgData import ImgData
import math
import sys

MAX_FEATURES = 1000

class Features:
    traced = True

    def __init__(self, theReference, theTentative):
        self.imgReference = theReference
        self.imgTentative= theTentative
        self.imgTentative = self.scaleTentativeImageToDimensionsOfReference(self.imgReference, self.imgTentative)
        self.dataReference = ImgData('reference', self.imgReference)
        self.dataTentative = ImgData('tentative', self.imgTentative)

    def extractFeatures(self):
      self.dataReference.calculateIntrinsicData()
      self.dataTentative.calculateIntrinsicData()

      if(self.dataTentative.meanDistance()!= 0 ):
        scaleFactor = self.dataReference.meanDistance()/self.dataTentative.meanDistance()
        output("Scale factor is "+ str(scaleFactor))
      if(scaleFactor!=1):
          if(self.traced):
            output("Applying scale factor")
          self.dataTentative.scalePoints(scaleFactor)
      self.findRotation()
        
    def findRotation(self):
        offset = self.findOffset();
        max_value = 0
        max_angle = 0 ;
        self.dataTentative.prepareDataForTest()
        for angle in range(360):
            #angle = 0;
            #while(angle >-180):
            referencePointsRotated = self.dataReference.generatePointsForAngle(offset, angle)
            #referenceRotated = self.dataReference.generateForAngle(offset, angle)
            #self.dataTentative.show('ref rotated ' +str(angle), referenceRotated);
            #self.dataTentative.show('tentative', self.dataTentative.image);
            #valueForAngle = self.dataTentative.testForAngle(referenceRotated)
            valueForAngle = self.dataTentative.testPointsForAngle(referencePointsRotated)
            #self.dataTentative.showForAngle(referenceRotated, 'angle: '+str(angle))
            print(" test angle is:"+ str(angle)+" value is:"+str(valueForAngle))
            if(valueForAngle>max_value):
                max_value = valueForAngle
                max_angle = angle
            #angle -= 45
        print("Angle is:"+ str(max_angle)+" value is:"+str(max_value))
        print("Offset is:"+ str(offset.x)+" / "+str(offset.y))
        return max_value;
        
    def findOffset(self):
        offsetX = self.dataTentative.centerOfMass().x - self.dataReference.centerOfMass().x
        offsetY = self.dataTentative.centerOfMass().y - self.dataReference.centerOfMass().y
        return APoint(offsetX,  offsetY);

    def scaleTentativeImageToDimensionsOfReference(self, imgReference, imgTentative):
        #todo
        return imgTentative

    def scaleTentativeImageToDimensionsOfReference1(self, imgReference, imgTentative):
        print imgReference.shape
        pass
        heightReference, widthReference, _ = imgReference.shape
        heightTentative, widthTentative, _ = imgTentative.shape
        if((heightReference==heightTentative) and (widthReference==widthTentative)):
            return imgTentative
        imgResized = cv2.resize(imgTentative, (widthReference, heightReference))
        if(self.traced):
            output('Resized to: '+str(imgResized.shape[1])+'/'+str(imgResized.shape[0]))
        return imgResized;

def output(arg):
    print arg
