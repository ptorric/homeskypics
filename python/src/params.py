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

import sys, getopt

class Params:
    traced = False

    def __init__(self):
        pass

    def decode(self, args):
        self.do_video = False
        self.output = "../data/output"
        try:
            opts, args = getopt.getopt(args,"vo:",["video","output="])
        except getopt.GetoptError:
            print ('main.py -v -o output_folder')
            return
        for opt, arg in opts:
          if opt == '-v':
             self.do_video = True
          elif opt in ("-o", "--output"):
             self.output = arg
        if( self.traced ):
            print ('video: "'+ str(self.do_video));
            print ('Output file is "'+ self.output+'"')
