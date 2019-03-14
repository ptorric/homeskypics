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
import cv2

class Loader:
    def __init__(self):
        pass

    def loadReferenceAndTentative(self):
        self.loadTest5();
        self.check();

    def check(self):
        if( self.imgGrayReference is None ):
            raise RuntimeError('Gray Reference image could not be loaded.')
        if( self.imgColorReference is None ):
            raise RuntimeError('Color Reference image could not be loaded.')
        if( self.imgGrayTentative is None ):
            raise RuntimeError('Gray Tentative image could not be loaded.')
        if( self.imgGrayTentative is None ):
            raise RuntimeError('Color Tentative image could not be loaded.')

    def loadReference(self, imagePath):
        self.imgGrayReference = cv2.imread(imagePath,cv2.IMREAD_GRAYSCALE)
        self.imgColorReference = cv2.imread(imagePath,cv2.IMREAD_COLOR)

    def loadTentative(self, imagePath):
        self.imgGrayTentative = cv2.imread(imagePath,cv2.IMREAD_GRAYSCALE)
        self.imgColorTentative = cv2.imread(imagePath,cv2.IMREAD_COLOR)

    def loadTest5(self):
        self.loadReference('../data/sample/IMG_0589.jpg')
        self.loadTentative('../data/sample/IMG_0590.jpg')

    def loadTestSelf(self):
        self.loadReference('../data/sample/IMG_0589.jpg')
        self.loadTentative('../data/sample/IMG_0589.jpg')

    def loadTest1(self):
        self.loadReference('../data/sample/i0.png')
        self.loadTentative('../data/sample/i1.png')

    def loadTest2(self):
        self.loadReference('../data/sample/test1.jpg')
        self.loadTentative('../data/sample/test2.jpg')

    def loadTest3(self):
        self.loadReference('../data/sample/points0.png')
        self.loadTentative('../data/sample/points0moved.png')

    def loadTest4(self):
        self.loadReference('../data/sample/points0.png')
        self.loadTentative('../data/sample/points0rot.png')
