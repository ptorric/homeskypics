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
import util

NUM_ITERATIONS_EROSION=6

class Cleaner:

    traced = False
    writeOp = False ;

    def __init__(self):
        self.iterationsErosion = NUM_ITERATIONS_EROSION

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

    def prepare(self, img, id):
        imgf = cv2.GaussianBlur(img,(5,5),0);
        if(self.writeOp):
            util.show('blurred',imgf)
        return imgf;

    def clean(self, img, id):
        if(self.writeOp):
            util.show('orig',img)
        imgf = self.prepare(img, 'orig');
        if(self.writeOp):
            util.show('prepared',imgf)
        soglia = self.calcHistogramTrhreshold(imgf);
        nuova_soglia = soglia ;
        num_points = 10000;
        while(num_points>100):
            nuova_soglia = nuova_soglia +1 ;
            num_points = self.calculatePoints(imgf, nuova_soglia)
            if(self.writeOp):
                util.output("Test for threshold "+ str(nuova_soglia)+" Points #: "+ str(num_points));
            if(num_points <= 0):
                nuova_soglia = nuova_soglia -1 ;
                break;
        self.soglia = nuova_soglia;
        return num_points, self.applyThreshold(imgf, self.soglia)

    def cleanWithExpectedCount(self, img, id, target):
        if(self.writeOp):
            util.show('orig',img)
        imgf = self.prepare(img, 'orig');
        if(self.writeOp):
            util.show('prepared',imgf)
        num_points = 0;
        target_value = int(target*1.1)
        nuova_soglia = 256
        while((num_points<target_value) and (nuova_soglia>=0) ):
            nuova_soglia = nuova_soglia -1 ;
            num_points = self.calculatePoints(imgf, nuova_soglia)
            if(self.writeOp):
                util.output("Test for threshold "+ str(nuova_soglia)+" Points #: "+ str(num_points));
        self.soglia = nuova_soglia+1;
        return self.applyThreshold(imgf, self.soglia)

    def calculatePoints(self, imgf, threshold):
        imgf = self.applyThreshold(imgf, threshold)
        imgInverted = cv2.bitwise_not(imgf)
        if(self.traced):
            util.show('Tracing this', imgInverted)
        mum_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(imgInverted)
        return mum_labels -1 ;

    def calcHistogramTrhreshold(self, imgf):
        hist = cv2.calcHist([imgf],[0],None,[256],[0,256])
        threshold = 255
        bins = len(hist)
        index = 0
        total = 0;
        while( index < bins ):
            if(self.traced):
                util.output("hist "+ str(index)+ " value "+ str(hist[index]))
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
        if(self.traced):
            util.output("Threshold is "+str(threshold));
        if( threshold >= 254 ):
            threshold = 254
        else:
            threshold += 1
        self.threshold = threshold
        if(self.traced):
            util.show('before tresh', imgf)
        return threshold;

    def applyThreshold(self, imgf, threshold):
        _, imgf = cv2.threshold(imgf,threshold,255,cv2.THRESH_BINARY)
        if(self.traced):
            util.show('after tresh', imgf)
        imgf = cv2.bitwise_not(imgf)
        imgf = self.dilatation(imgf, id, 1)
        return imgf

