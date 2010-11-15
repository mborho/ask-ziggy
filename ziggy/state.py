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

    def __init__(self, services):
        self.services = services
        self.services_active = services[0:]
        self.deli_pop = 0
        self.direct_linkage = False
        self.use_proxy = False
        self.mobilizer = False
        self.hide_quick = False
        self.history_len = 10
        self.buffers = {}
        self.langs = {}
        self.tlate = {}
        self.history = {}
        self.default_langs = {}
        self.config_file = os.path.expanduser("~")+"/.ask-ziggy"
        self.load()    

    def normalize_active_services(self):
        ''' active services list should be simple list '''
        result = []
        for s in self.services_active:
            service = s[0] if type(s) == list else s
            result.append(service)        
        self.services_active = result if result else self.services_active
        
    def validate_services(self,  saved_services):
        ''' check loaded services '''
        result = []
        # check for new services
        for s in self.services:
            if  s not in saved_services:
                saved_services.append(s)
                self.services_active.append(s)
        # check for removed services
        for s in saved_services:
            if  s not in self.services:
                saved_services.remove(s)
                if s in self.services_active:
                    self.services_active.remove(s)
        return saved_services

    def load(self):
        try:
            f = open(self.config_file,'a+')
            json = f.read()
            f.close()
            data = simplejson.loads(json)
            self.history = data.get('history',{})
            self.direct_linkage = data.get('direct_linkage', self.direct_linkage)
            self.use_proxy = data.get('use_proxy', self.use_proxy)
            self.mobilizer = data.get('mobilizer', self.mobilizer)
            self.hide_quick = data.get('hide_quick', self.hide_quick)
            self.history_len = data.get('history_len', self.history_len)
            self.default_langs = data.get('default_langs', {})
            self.services_active = data.get('services_active',self.services_active) 
            saved_services = data.get('services',self.services)
            self.services = self.validate_services(saved_services)
            self.normalize_active_services()
        except:
            print "no file found"
        
    def save(self):
        state = {
            'history':self.history, 'history_len': self.history_len,
            'services_active': self.services_active,  'services':self.services,
            'direct_linkage': self.direct_linkage, 'use_proxy':self.use_proxy, 
            'default_langs': self.default_langs, 'mobilizer':self.mobilizer,
            'hide_quick': self.hide_quick}
        f = open(self.config_file,'w')
        simplejson.dump(state, f)
        f.close()
