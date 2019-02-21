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
from aPoint import APoint
import cv2
import numpy as np
import math

CONNECTIONS=8
DISTANCE_THRESHOLD=8

class ImgData:

    traced = False
    tracedNow = True

    def __init__(self, theName, theImage):
        self.name = theName
        self.image = theImage
        self.cm = APoint(0,0)
        self.height, self.width = self.image.shape
        if(self.traced):
            show(self.name, self.image);

    def setPoints(self, newPoints):
        self.points = newPoints

    def centerOfMass(self):
        return self.cm;

    def calculateCenterOfMass(self):
        sumX = 0;
        sumY = 0;
        index = 0;
        for _, point in enumerate(self.points):
            sumX += point.x*point.weight
            sumY += point.y*point.weight
            index+=1;
        if(index>0):
            self.cm = APoint(sumX/index, sumY/index)
        else:
            self.cm = APoint(0,0)
        return self.cm;

    def calculateMeanDistance(self):
        self._meanDistance = 0;
        cumulative = 0
        index = 0;
        deltaX = 0;
        deltaY = 0;
        for _, point in enumerate(self.points):
            deltaX += point.x - self.cm.x
            deltaY += point.y - self.cm.y
            cumulative += math.sqrt(deltaX*deltaX+deltaY*deltaY)
            index+=1;
        if(index>0):
            self._meanDistance = cumulative/index;
        return self._meanDistance;

    def meanDistance(self):
        return self._meanDistance

    def calculateIntrinsicData(self):
        self.extractFeatures()
        self.calculateCenterOfMass()
        self.calculateMeanDistance()

    def extractFeatures(self):
        imgInverted = cv2.bitwise_not(self.image)
        #imgInverted = self.image
        if(self.traced):
            show('Tracing this', imgInverted)
        mum_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imgInverted)
        self.points = list()
        if(self.traced):
            print(set(labels.reshape(-1).tolist()))
            output(str(centroids))
            output(str(labels))
            output(str(stats))
            output (' Labels count: '+str(mum_labels))
        for i in range(mum_labels):
            # skip 0 item
            if(i!=0):
                point = APoint(centroids[i][0], centroids[i][1])
                self.points.append(point)
                if(self.traced):
                    output ('Found: '+str(i)+' at:'+str(point.x)+'/'+str(point.y))
        if(self.traced):
            self.showPoints(self.image, self.points)

    def scalePoints(self, scaleFactor):
        pass
        
    def blankImage(self):
        newImage = np.full( (self.height, self.width, 1), 255, np.uint8 )
        return newImage

    def markObjectInImage(self, image, point):
        print(" setting:"+str(point.x)+"/"+str(point.y))
        #Normalizza i punti allargando lo spettro
        self.setPoint( image, point.x-1, point.y-1, 0)
        self.setPoint( image, point.x, point.y-1, 0)
        self.setPoint( image, point.x+1, point.y-1, 0)
        #
        self.setPoint( image, point.x-1, point.y, 0 )
        self.setPoint( image, point.x, point.y, 0 )
        self.setPoint( image, point.x+1, point.y, 0 )
        #
        self.setPoint( image, point.x-1, point.y+1, 0)
        self.setPoint( image, point.x, point.y+1, 0)
        self.setPoint( image, point.x+1, point.y+1, 0)
        cv2.circle( image, (int(point.x), int(point.y)), 10, 0, 2)

    def prepareDataForTest(self):
        self.imageWithObjectCenters = self.blankImage();
        #Normalizza i punti allargando lo spettro
        for _, point in enumerate(self.points):
            self.markObjectInImage(self.imageWithObjectCenters, point)
        if(self.tracedNow):
            self.show('prepared', self.imageWithObjectCenters)

    def generateForAngle(self, offsetAsPoint, angle):
        imgToTest = self.blankImage();
        for _, point in enumerate(self.points):
            print(" in:"+str(point.x)+"/"+str(point.y)+" angle:"+str(angle))
            pointMoved = self.moveScalePoint(point, offsetAsPoint, angle)
            print(" out:"+str(pointMoved.x)+"/"+str(pointMoved.y))
            self.markObjectInImage(imgToTest, pointMoved);
        return imgToTest

    def generatePointsForAngle(self, offsetAsPoint, angle):
        points = list();
        for _, point in enumerate(self.points):
            pointMoved = self.moveScalePoint(point, offsetAsPoint, angle)
            points.append(pointMoved)
        return points

    def testForAngle(self, imgToDetect):
        # TODO: use bitwise_and and histogram
        value = 0
        for row in range(self.height):
            for col in range(self.height):
                if((0==self.imageWithObjectCenters[row][col])or(0==imgToDetect[row][col])):
                    value += 1
        return value

    def distance2(self, point, otherPoint):
        x = point.x - otherPoint.x
        y = point.y - otherPoint.y
        return x*x+y*y

    def testPointsForAngle(self, pointsToEvaluate):
        # TODO: use bitwise_and and histogram
        value = 0
        for _, point in enumerate(self.points):
            for _, otherPoint in enumerate(pointsToEvaluate):
                if(self.distance2(point, otherPoint)<DISTANCE_THRESHOLD):
                    value += 1
        return value

    def showForAngle(self, imgToDetect, id):
        # TODO: use bitwise_and and histogram
        imgNew = imgToDetect.copy()
        value = 0
        for row in range(self.height):
            for col in range(self.height):
                if((0==self.imageWithObjectCenters[row][col])or(0==imgToDetect[row][col])):
                    imgNew[row][col] = 0
        show(id, imgNew)

    def moveScalePoint(self, point, offsetAsPoint, angle):
        #TODO: refactor, move out constants
        angleInRadians = math.radians(angle)
        new_mass_center_x = self.cm.x + offsetAsPoint.x
        new_mass_center_y = self.cm.y + offsetAsPoint.y
        delta_x = point.x - self.cm.x
        delta_y = point.y - self.cm.y
        cosAngle = math.cos(angleInRadians)
        sinAngle = math.sin(angleInRadians)
        new_x = new_mass_center_x + cosAngle * delta_x - sinAngle * delta_y
        new_y = new_mass_center_y + sinAngle * delta_x + cosAngle * delta_y
        return APoint(new_x, new_y);

    def setPoint(self, img, the_x, the_y, value) :
        x = int(the_x)
        y = int(the_y)
        if((x<self.width) and (x>=0) and (y<self.height) and (y>=0)):
            img[y][x] = value

    def showPoints(self, img, keypoints) :
        imgColor = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        color = (0,0,255)
        for pt in keypoints:
            startX = int(pt.x)
            startY = int(pt.y)
            cv2.circle(imgColor, (startX, startY), 4, color)
        show("Matches", imgColor)

    def show(self, id, img):
        show(self.name+': '+id,img)

def output(arg):
    print arg

def show(id, img):
    output('Dimensions of '+id+' are: '+str(img.shape[1])+'/'+str(img.shape[0]))
    cv2.imshow(id,img)
    cv2.waitKey(0)

def emptyImage(width, height):
    newImage = np.full( (height, width, 1), 255, np.uint8 )
    return newImage
