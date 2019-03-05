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
from apoint import APoint
import numpy as np
import cv2
import imgdata
from imgdata import ImgData
import math
import sys
import util

class Features:
    traced = True

    def __init__(self, theGrayReference, theColorReference, theGrayTentative, theColorTentative):
        self.imgReference = theGrayReference
        self.imgTentative = theGrayTentative
        self.imgColorReference = theColorReference
        self.imgColorTentative = theColorTentative
        self.imgTentative = self.scaleTentativeImageToDimensionsOfReference(self.imgReference, self.imgTentative)
        self.dataReference = ImgData('reference', self.imgReference)
        self.dataTentative = ImgData('tentative', self.imgTentative)

    def extractFeatures(self):
      self.dataReference.calculateIntrinsicData()
      self.dataTentative.calculateIntrinsicData()
      if(self.traced):
          self.print_cm()

      if(self.dataReference.meanDistance()!= 0 ):
        scaleFactor = self.dataTentative.meanDistance()/self.dataReference.meanDistance()
        output("Scale factor is "+ str(scaleFactor))
      if(scaleFactor!=0):
          if(self.traced):
            output("Applying scale factor")
          self.dataReference.scalePoints(scaleFactor)
      if(self.traced):
          self.print_cm()
      value, angle = self.findRotation()
        
    def findRotation(self):
        self.offset = self.findOffset();
        print("Offset is:"+ str(self.offset.x)+" / "+str(self.offset.y))
        max_value = 0
        max_angle = 0 ;
        start_angle, threshold = self.findRotationCoarse();
        self.showRotation(threshold)
        for angle_index in range( start_angle-5, start_angle+5):
            if(angle_index < 0):
                angle = angle_index + 360
            else:
                angle = angle_index
            referencePointsRotated = self.dataReference.generatePointsForAngle(self.offset, angle)
            valueForAngle = self.dataTentative.testPointsForAngle(referencePointsRotated, imgdata.DISTANCE_FINE)
            #self.dataTentative.showForAngle(referenceRotated, 'angle: '+str(angle))
            self.writeImageForAngle(self.offset, angle)
            if(self.traced):
                print(" test angle is:"+ str(angle)+" value is:"+str(valueForAngle))
            if(valueForAngle>max_value):
                max_value = valueForAngle
                max_angle = angle
            if(angle<10):
                angle += 1
            else:
                angle += 10
        print("Angle is:"+ str(max_angle)+" value is:"+str(max_value))
        self.imageReferenceRotatedWithPoints = self.dataReference.generateForAngleAndOffset(self.offset, angle)
        #self.imageReferenceRotated = self.dataReference.generateForAngleAndOffset(offset, angle)
        return max_value, max_angle;


    def findRotationCoarse(self):
        threshold = imgdata.DISTANCE_COARSE
        one_tenth_points = len(self.dataReference.points)/10
        not_good = True
        while(not_good):
            max_value = 0
            max_angle = 0 ;
            angle = 0;
            print("****Testing threshold:"+str(threshold))
            while(angle <360):
                referencePointsRotated = self.dataReference.generatePointsForAngle(self.offset, angle)
                valueForAngle = self.dataTentative.testPointsForAngle(referencePointsRotated, threshold)
                if(self.traced):
                    print(" test angle is:"+ str(angle)+" value is:"+str(valueForAngle))
                if(valueForAngle>max_value):
                    max_value = valueForAngle
                    max_angle = angle
                angle += 10
            print("Coarse Angle is:"+ str(max_angle)+" value is:"+str(max_value))
            if((max_value>one_tenth_points) or (threshold >= imgdata.DISTANCE_MAX )):
                not_good = False
            else:
                threshold += imgdata.DISTANCE_STEP;
            #self.imageReferenceRotatedWithPoints = self.dataReference.generateForAngleAndOffset(self.offset, angle)
            #self.imageReferenceRotated = self.dataReference.generateForAngleAndOffset(offset, angle)
        return max_angle, threshold;


    def showRotation(self, threshold):
        #video = cv2.VideoWriter('../data/out/animation.avi', cv2.VideoWriter_fourcc(*'X264'), 25, (self.dataReference.width, self.dataReference.height))
        video = cv2.VideoWriter('../data/out/animation.avi', cv2.VideoWriter_fourcc(*'XVID'), 3, (self.dataReference.width, self.dataReference.height))

        self.offset = self.findOffset();
        max_value = 0
        max_angle = 0 ;
        angle = 0;
        while(angle <360):
            referencePointsRotated = self.dataReference.generatePointsForAngle(self.offset, angle)
            valueForAngle = self.dataTentative.testPointsForAngle(referencePointsRotated, threshold)
            if(valueForAngle>max_value):
                max_value = valueForAngle
                max_angle = angle
            img = self.createImageForAngle(self.offset, angle)
            cv2.putText(img, 'Angle:'+str(angle)+ " value:"+str(valueForAngle)+ " max:"+str(max_angle), (30,30), cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 3)
            video.write(img)
            angle += 1
            print("Video: "+str(angle)+"/360");
        video.release()

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

    def showSuperImposedImages(self, offset, angle):
        cols = self.dataReference.width;
        rows = self.dataReference.height
        #rotation
        rotation = cv2.getRotationMatrix2D((self.dataReference.cm.x,self.dataReference.cm.y),angle,1)
        rotated = cv2.warpAffine(self.dataReference.image,rotation,(cols,rows))
        # translate reference
        translation = np.float32([[1,0,int(offset.x)],[0,1,int(offset.y)]])
        rotatedAndTranslated = cv2.warpAffine(rotated, translation, (cols, rows))
        colorTentative = cv2.cvtColor(self.dataTentative.image, cv2.COLOR_GRAY2BGR)
        #colorTentative = self.dataTentative.image
        #rotatedAndTranslated = cv2.cvtColor(rotatedAndTranslated, cv2.COLOR_GRAY2BGR)
        rotatedAndTranslated = cv2.cvtColor(rotatedAndTranslated, cv2.COLOR_GRAY2BGR)
        #rotatedAndTranslated = rotated
        print( rotatedAndTranslated.shape)
        print( colorTentative.shape)
        finalImage = cv2.addWeighted(rotatedAndTranslated, 0.7, colorTentative, 0.3, 0)
        #finalImage = rotated
        #finalImage = cv2.cvtColor(finalImage, cv2.COLOR_GRAY2BGR)
        self.dataReference.drawDestinationPoints(finalImage, offset, angle, self.dataTentative.hits, self.dataTentative.points, self.dataReference.cm)

        util.show('final', finalImage)

    def createImageForAngle(self, offset, angle):
        image = self.imgColorTentative.copy()
        self.dataReference.drawDestinationPoints(image, offset, angle, self.dataTentative.hits, self.dataTentative.points, self.dataTentative.cm)
        return image;

    def writeImageForAngle(self, offset, angle):
        image = self.createImageForAngle(offset, angle)
        cv2.imwrite('../data/out/'+str(angle)+'.png', image, [cv2.IMWRITE_PNG_COMPRESSION, 0])

    def showAllImages(self, offset, angle):
        util.show('Reference', self.dataReference.imgWithPointsAndMassCenter())
        util.show('Tentative', self.dataTentative.imgWithPointsAndMassCenter())
        self.showSuperImposedImages(offset, angle)

    def print_cm(self):
        print("reference cm "+str(self.dataReference.cm))
        print("tentative cm "+str(self.dataTentative.cm))


def output(arg):
    print arg
