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
        pass;

    def loadReferenceAndTentative(self):
        self.loadTest2();

    def loadTest1(self):
        self.imgReference = cv2.imread('../data/sample/i0.png',cv2.IMREAD_GRAYSCALE)
        self.imgTentative = cv2.imread('../data/sample/i1.png',cv2.IMREAD_GRAYSCALE)

    def loadTest2(self):
        self.imgReference = cv2.imread('../data/sample/test1.jpg',cv2.IMREAD_GRAYSCALE)
        self.imgTentative = cv2.imread('../data/sample/test2.jpg',cv2.IMREAD_GRAYSCALE)

    def reference(self):
         return self.imgReference ;

    def tentative(self):
        return self.imgTentative ;
