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
from imgdata import ImgData
import math
import sys

def output(arg):
    print arg

def emptyImage(width, height):
    newImage = np.full( (height, width, 1), 255, np.uint8 )
    return newImage

def emptyColorImage(width, height):
    newImage = np.full( (height, width, 3), 255, np.uint8 )
    return newImage

def show(id, img):
    output('Dimensions of '+id+' are: '+str(img.shape[1])+'/'+str(img.shape[0]))
    cv2.imshow(id,img)
    cv2.waitKey(0)
