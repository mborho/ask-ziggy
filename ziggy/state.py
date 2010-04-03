#!/usr/bin/env python
# -*- coding: utf-8 -*-
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published
## by the Free Software Foundation; version 3 only.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
# Copyright 2010 Martin Borho <martin@borho.net>
import os
import simplejson

class AppState(object):

    def __init__(self):
        self.deli_pop = 0
        self.buffers = {}
        self.langs = {}
        self.tlate = {}
        self.history = {}
        self.config_file = os.path.expanduser("~")+"/.ask-ziggy"
        self.load()

    def load(self):
        try:
            f = open(self.config_file,'a+')
            json = f.read()
            f.close()
            data = simplejson.loads(json)
            self.history = data.get('history',{})
        except:                
            print "no file found"
        
    def save(self):
        state = {'history':self.history}
        f = open(self.config_file,'w')
        simplejson.dump(state, f)
        f.close()