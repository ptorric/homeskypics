#!/usr/bin/env python
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
import numpy as np
import cv2
import sys

NUM_ITERATIONS_EROSION=6

class Cleaner:

    traced = False
    writeOp = False ;

    def __init__(self):
        self.iterationsErosion = NUM_ITERATIONS_EROSION

    def clean1(self, img, id):
        imgf = cv2.bitwise_not(img)
        if(self.writeOp):
            cv2.imwrite("output/clean_binario"+id+".png", imgf );
        imgf = self.threshold(imgf, id)
        if(self.writeOp):
            cv2.imwrite("output/clean_soglia"+id+".png", imgf );
        imgf = self.reduction(imgf, id, self.iterationsErosion)
        if(self.writeOp):
            cv2.imwrite("output/clean_reduction"+id+".png", imgf );
        return imgf

    def reduction(self, img, id, theIterations):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
        imgf = cv2.erode(img, kernel, iterations=theIterations)
        imgf = cv2.dilate(imgf, kernel, iterations=theIterations)
        return imgf

    def dilatation(self, img, id, theIterations):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        imgf = cv2.dilate(img, kernel, iterations=theIterations)
        return imgf

    def erosion(self, img, id, theIterations):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        imgf = cv2.erode(img, kernel, iterations=theIterations)
        return imgf

    def thresholdOTSU(self, img, id):
        ret, imgf = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        return imgf

    def thresholdAdaptive(self, img, id):
        imgf = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        return imgf

    def threshold(self, img, id):
        imgf = self.thresholdOTSU(img, id)
        return imgf

    def clean(self, img, id):
        if(self.writeOp):
            self.show('orig',img)
        imgf = cv2.GaussianBlur(img,(5,5),0);
        if(self.writeOp):
            self.show('blurred',imgf)

        hist = cv2.calcHist([imgf],[0],None,[256],[0,256])
        threshold = 255
        bins = len(hist)
        index = 0
        total = 0;
        while( index < bins ):
            if(self.traced):
                output("hist "+ str(index)+ " value "+ str(hist[index]))
            total += hist[index]
            index += 1;
        soglia = total * 0.005 ;
        index = bins -1
        cumulative = 0
        while( index > 0 ):
            cumulative += hist[index]
            if( cumulative > soglia ):
                break;
            threshold -= 1
            index -= 1
        print threshold
        #if( threshold < 75 ):
        #    threshold = 75
        if( threshold == 255 ):
            threshold = 254
        if(self.traced):
            self.show('before tresh', imgf)
        _, imgf = cv2.threshold(imgf,threshold,255,cv2.THRESH_BINARY)
        if(self.traced):
            self.show('after tresh', imgf)
        imgf = cv2.bitwise_not(imgf)
        #cv2.imshow('soglia',imgf)
        #cv2.waitKey(0)

        #imgf = cv2.bitwise_not(img)
        #if(self.writeOp):
        #    cv2.imwrite("output/clean_binario"+id+".png", imgf );
        #imgf = self.threshold(imgf, id)
        #if(self.writeOp):
        #    cv2.imwrite("output/clean_soglia"+id+".png", imgf );
        imgf = self.dilatation(imgf, id, 1)
        #cv2.imshow('filtro',imgf)
        #cv2.waitKey(0)
        #if(self.writeOp):
        #    cv2.imwrite("output/clean_reduction"+id+".png", imgf );
        #sys.exit();
        return imgf

    def show(self, id, img):
        cv2.imshow(id,img)
        cv2.waitKey(0)

def output(arg):
    print arg
