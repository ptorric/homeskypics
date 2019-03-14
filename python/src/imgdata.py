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
from apoint import APoint
from angledata import AngleData
import cv2
import numpy as np
import math

CONNECTIONS=8
# 15 px distant: 825, 10px: 100, 8:64
DISTANCE_FINE=100
DISTANCE_COARSE=400
DISTANCE_MAX=1000
DISTANCE_STEP=100

class ImgData:

    traced = False
    tracedNow = True

    def __init__(self, theName, theImage):
        self.name = theName
        self.image = theImage
        self.cm = APoint(0,0)
        self.hits = list()
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
            self.cm = APoint(int(sumX/index), int(sumY/index))
        else:
            self.cm = APoint(0,0)
        return self.cm;

    def calculateMeanDistanceLinear(self):
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

    def calculateMeanDistanceWeighted(self):
        self._meanDistance = 0;
        cumulative = 0
        index = 0;
        deltaX = 0;
        deltaY = 0;
        max_distance = 0
        for _, point in enumerate(self.points):
            deltaX += point.x - self.cm.x
            deltaY += point.y - self.cm.y
            distance = math.sqrt(deltaX*deltaX+deltaY*deltaY)
            if(distance>max_distance):
                max_distance = distance
            cumulative += math.sqrt(deltaX*deltaX+deltaY*deltaY)
            index+=1;
        #repeat using the distance as a weight
        cumulative = 0
        index = 0;
        deltaX = 0;
        deltaY = 0;
        for _, point in enumerate(self.points):
            deltaX += point.x - self.cm.x
            deltaY += point.y - self.cm.y
            distance = math.sqrt(deltaX*deltaX+deltaY*deltaY)
            weight = distance/max_distance
            cumulative += weight*math.sqrt(deltaX*deltaX+deltaY*deltaY)
            index+=weight;
        if(index>0):
            self._meanDistance = cumulative/index;
        return self._meanDistance;

    def calculateMeanDistance(self):
        return self.calculateMeanDistanceWeighted()

    def meanDistance(self):
        return self._meanDistance

    def calculateIntrinsicData(self):
        self.extractFeatures()
        self.originalPoints = self.points;
        self.calculateCenterOfMass()
        self.calculateMeanDistance()

    def extractFeatures(self):
        imgInverted = cv2.bitwise_not(self.image)
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
        scaledPoints = list()
        for _, point in enumerate(self.points):
            len_x = scaleFactor*(point.x - self.cm.x)
            len_y = scaleFactor*(point.y - self.cm.y)
            newPoint = APoint(len_x+self.cm.x, len_y+self.cm.y)
            scaledPoints.append(newPoint);
        self.points = scaledPoints ;

    def blankImage(self):
        newImage = np.full( (self.height, self.width, 1), 255, np.uint8 )
        return newImage

    def markObjectInImage(self, image, point):
        #print(" setting:"+str(point.x)+"/"+str(point.y))
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

    def generateForAngleAndOffset(self, offsetAsPoint, angle):
        imgToTest = self.blankImage();
        angleData = AngleData(angle)
        for _, point in enumerate(self.points):
            #print(" in:"+str(point.x)+"/"+str(point.y)+" angle:"+str(angle))
            pointMoved = self.moveScalePointOp(point, offsetAsPoint, angleData)
            #print(" out:"+str(pointMoved.x)+"/"+str(pointMoved.y))
            self.markObjectInImage(imgToTest, pointMoved);
        return imgToTest

    def generatePointsForAngle(self, offsetAsPoint, angle):
        points = list();
        angleData = AngleData(angle)
        for _, point in enumerate(self.points):
            pointMoved = self.moveScalePointOp(point, offsetAsPoint, angleData)
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

    def testPointsForAngle(self, pointsToEvaluate, distance):
        if(self.traced):
            print ("*****Testing points")
        hits = list()
        value = 0
        for point in self.points:
            for otherPoint in pointsToEvaluate:
                if(self.traced):
                    distance = self.distance2(point, otherPoint)
                    print ("Testing this "+str(point)+ " other:"+str(otherPoint)+ " distance:" +str(distance));
                if(self.distance2(point, otherPoint)<distance):
                    hits.append(point);
                    value += 1
        self.hits = hits
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
        return self.moveScalePointOp(self, point, offsetAsPoint, AngleData(angle))

    def moveScalePointOp(self, point, offsetAsPoint, angleData):
        #TODO: refactor, move out constants
        new_mass_center_x = self.cm.x + offsetAsPoint.x
        new_mass_center_y = self.cm.y + offsetAsPoint.y
        delta_x = point.x - self.cm.x
        delta_y = point.y - self.cm.y
        new_x = new_mass_center_x + (angleData.cosAngle * delta_x) - (angleData.sinAngle * delta_y)
        new_y = new_mass_center_y + (angleData.sinAngle * delta_x) + (angleData.cosAngle * delta_y)
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

    def imgWithPointsAndMassCenter(self):
        colorImage = self.image.copy()
        colorImage = cv2.cvtColor(colorImage, cv2.COLOR_GRAY2BGR)
        color = (0,0,255)
        for pt in self.points:
            startX = int(pt.x)
            startY = int(pt.y)
            cv2.circle(colorImage, (startX, startY), 3, color)
        # cm
        colorCM = (0,255,0)
        cv2.line(colorImage, (self.cm.x, self.cm.y-20 ), (self.cm.x, self.cm.y+20 ), colorCM);
        cv2.line(colorImage, (self.cm.x-20, self.cm.y ), (self.cm.x+20, self.cm.y ), colorCM);
        return colorImage;

    def drawDestinationPoints(self, colorImage, offsetAsPoint, angle, hits, otherPoints, otherCM):
        go_new = True
        colorSrc = (255,0,255)
        colorDest = (0,255,255)
        colorOther = (0,255,0)
        colorLine = (255,128,0)
        colorHit = (0,0,255)
        colorOriginal = (255,0,0)
        colorCM = (255,255,255)
        colorCMOther = (0,0,255)
        for hit in hits:
            x = int(hit.x)
            y = int(hit.y)
            cv2.circle(colorImage, (x, y), 6, colorHit, 6)

        angleData = AngleData(angle);
        if(go_new):
            for pt in self.points:
                startX = int(pt.x)
                startY = int(pt.y)
                #cv2.line(colorImage, (self.cm.x, self.cm.y), (startX, startY), colorLine, 2)
                cv2.circle(colorImage, (startX, startY), 3, colorSrc)
                pointMoved = self.moveScalePointOp(pt, offsetAsPoint, angleData)
                endX = int(pointMoved.x)
                endY = int(pointMoved.y)
                cv2.circle(colorImage, (endX, endY), 6, colorDest)

        for pt in self.originalPoints:
            x = int(pt.x)
            y = int(pt.y)
            cv2.circle(colorImage, (x, y), 6, colorOriginal)

        for pt in otherPoints:
            x = int(pt.x)
            y = int(pt.y)
            cv2.circle(colorImage, (x, y), 6, colorOther)
            colorCM = (0,255,0)
        # cm
        drawCross(colorImage, self.cm, colorOriginal);
        # orig cm
        drawCross(colorImage, otherCM, colorOther);

        #print self.cm
        #print("this cm "+str(self.cm))
        #print("other cm "+str(otherCM))

    def drawOrigPointsAndCM(self, colorImage, offsetAsPoint, angle, other):
        colorSrc = (255,0,255)
        colorDest = (0,255,255)
        colorOther = (0,255,0)
        colorLine = (255,128,0)
        colorOriginal = (255,0,0)
        colorCM = (255,255,255)
        colorCMOther = (0,0,255)
        colorHit = (0,0,255)

        for hit in other.hits:
            x = int(hit.x)
            y = int(hit.y)
            cv2.circle(colorImage, (x, y), 6, colorHit, 3)

        for pt in self.originalPoints:
            x = int(pt.x)
            y = int(pt.y)
            cv2.circle(colorImage, (x, y), 6, colorOriginal)

        for pt in other.points:
            x = int(pt.x)
            y = int(pt.y)
            cv2.circle(colorImage, (x, y), 6, colorOther)
            colorCM = (0,255,0)
        # cm
        drawCross(colorImage, self.cm, colorCM);
        # orig cm
        drawCross(colorImage, other.cm, colorCMOther);
        #print("this cm "+str(self.cm))
        #print("other cm "+str(other.cm))

    def drawOriginalPointsAndCM(self, colorImage, other):
        colorOther = (0,0,255)
        colorOriginal = (0,255,0)
        colorHit = (0,255,255)

        for hit in other.hits:
            x = int(hit.x)
            y = int(hit.y)
            cv2.circle(colorImage, (x, y), 6, colorHit, 3)

        for pt in self.originalPoints:
            x = int(pt.x)
            y = int(pt.y)
            cv2.circle(colorImage, (x, y), 6, colorOriginal)

        for pt in other.points:
            x = int(pt.x)
            y = int(pt.y)
            cv2.circle(colorImage, (x, y), 3, colorOther)
            colorCM = (0,255,0)
        # cm
        drawCross(colorImage, self.cm, colorOriginal);
        # orig cm
        drawCross(colorImage, other.cm, colorOther);

def drawCross(image, point, color):
    cv2.line(image, (point.x, point.y-20 ), (point.x, point.y+20 ), color);
    cv2.line(image, (point.x-20, point.y ), (point.x+20, point.y ), color);

def output(arg):
    print (arg)

def show(id, img):
    output('Dimensions of '+id+' are: '+str(img.shape[1])+'/'+str(img.shape[0]))
    cv2.imshow(id,img)

def emptyImage(width, height):
    newImage = np.full( (height, width, 1), 255, np.uint8 )
    return newImage
