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
import numpy as np
from imgdata import ImgData
from apoint import APoint
from features import Features

class FeaturesTestCase(unittest.TestCase):

    def runTest(self):
        imgGray = np.full((10,10,1), 0, np.uint8)
        imgColor = np.full((10,10,3), 0, np.uint8)
        features = Features( imgGray, imgColor, imgGray, imgColor);

        features.dataTentative.cm = APoint(1, 2);
        features.dataReference.cm = APoint(10, 20);
        pt = features.findOffset()
        self.failUnless(pt.x == -9, 'offset centro di massa x errato: ' + str(pt.x))
        self.failUnless(pt.y == -18, 'offset centro di massa y errato: '+ str(pt.y))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(FeaturesTestCase("FeaturesTestCase"))
    return suite
