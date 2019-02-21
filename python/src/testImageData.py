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
import unittest
from imgData import ImgData
from aPoint import APoint
import numpy as np
import util

class ImgDataTestCaseCM(unittest.TestCase):

    def runTest(self):
        points = list();
        points.append(APoint(10, 100))
        points.append(APoint(20, 50))
        points.append(APoint(0, 0))
        imgData = ImgData('a', util.emptyImage(10, 10));
        imgData.setPoints(points)
        imgData.calculateCenterOfMass();
        cm = imgData.centerOfMass()
        self.failUnless(cm.x == 10, 'centro di X massa errato: ' + str(cm.x))
        self.failUnless(cm.y == 50, 'centro di Y massa errato: '+ str(cm.y))

#no move
class ImgDataTestMovePoint(unittest.TestCase):
    def runTest(self):
        imgData = imgDataWithCM(APoint(0,0))
        moved = imgData.moveScalePoint(APoint(5,10), APoint(0,0), 0)
        self.failUnless((moved.x == 5) and (moved.y == 10), '1')

# offset
class ImgDataTestMovePoint1(unittest.TestCase):
    def runTest(self):
        imgData = imgDataWithCM(APoint(0,0))
        moved = imgData.moveScalePoint(APoint(5,10), APoint(1,3), 0)
        self.failUnless((moved.x == 6) and (moved.y == 13), '2: ' + str(moved.x)+"/"+str(moved.y))

#rotation no offset
class ImgDataTestMovePoint2(unittest.TestCase):
    def runTest(self):
        imgData = imgDataWithCM(APoint(0,0))
        moved = imgData.moveScalePoint(APoint(5,10), APoint(0,0), -90)
        self.assertAlmostEqual(moved.x, 10, 1, '3x: ' + str(moved.x)+"/"+str(moved.y))
        self.assertAlmostEqual(moved.y, -5, 1, '3y: ' + str(moved.x)+"/"+str(moved.y))

#cm from origin
class ImgDataTestMovePoint3(unittest.TestCase):
    def runTest(self):
        imgData = imgDataWithCM(APoint(1,2))
        moved = imgData.moveScalePoint(APoint(5,10), APoint(0,0), 180)
        self.assertAlmostEqual(moved.x, -3, 1, '4x: ' + str(moved.x)+"/"+str(moved.y))
        self.assertAlmostEqual(moved.y, -6, 1, '4y: ' + str(moved.x)+"/"+str(moved.y))

#roto translation
class ImgDataTestMovePoint4(unittest.TestCase):
    def runTest(self):
        imgData = imgDataWithCM(APoint(1,2))
        moved = imgData.moveScalePoint(APoint(5,10), APoint(3,6), 180)
        self.assertAlmostEqual(moved.x, 0, 1, '4x: ' + str(moved.x)+"/"+str(moved.y))
        self.assertAlmostEqual(moved.y, 0, 1, '4y: ' + str(moved.x)+"/"+str(moved.y))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(ImgDataTestCaseCM("ImgDataTestCaseCM"))
    suite.addTest(ImgDataTestMovePoint("ImgDataTestMovePoint"))
    suite.addTest(ImgDataTestMovePoint1("ImgDataTestMovePoint1"))
    suite.addTest(ImgDataTestMovePoint2("ImgDataTestMovePoint2"))
    suite.addTest(ImgDataTestMovePoint3("ImgDataTestMovePoint3"))
    suite.addTest(ImgDataTestMovePoint4("ImgDataTestMovePoint4"))
    return suite

def imgDataWithCM(newCM):
    imgData = ImgData('a', util.emptyImage(10, 10));
    imgData.cm = newCM ;
    return imgData
