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
from loader import Loader
from cleaner import Cleaner
from features import Features
import sys

if __name__ == '__main__':

  loader = Loader();
  loader.loadReferenceAndTentative();
  cleaner = Cleaner();
  imgReference = cleaner.clean(loader.imgGrayReference, "reference")
  imgTentative = cleaner.clean(loader.imgGrayTentative, "tentative")

  features = Features(imgReference, loader.imgColorReference, imgTentative, loader.imgColorTentative);
  features.extractFeatures()

  sys.exit();
