#!/usr/bin/env python

# Copyright 2008 - Michael Brunton-Spall
# This defines a memory map for a virtual machine

import logging

memorymap = []
HEADER = 0
DYNAMIC = 1
STATIC = 2
HIGH = 3
NONE = 4

class ReadOnlyException:
    def __init__(self, location=None):
        self.location = location
    def __str__(self):
        return "Memory at address 0x%x is read only" % self.location
    
class OutOfRangeException:
    def __init__(self, location=None):
        self.location = location
    def __str__(self):
        return "Memory at address 0x%x is in the high memory region" % self.location

class Memory:
    def __init__(self, bytes = None):
        self.version = 8
        self.memorymap = bytes
        if self.memorymap == None:
            self.memorymap = []
    def size(self):
        return len(self.memorymap)
    def set_version(self, version):
        self.version = version
    def high_mem_start(self):
        return self.get_byte(0x04)
    def static_mem_start(self):
        return self.get_byte(0x0e)
    def get_type_at(self, address):
        if address < 64: return HEADER
        if address >= self.size(): return NONE
        if address >= 64 and address < self.static_mem_start(): return DYNAMIC
        if address >= self.static_mem_start() and address < self.high_mem_start(): return STATIC
        return HIGH
    def _put_byte(self, location, b):
        self.memorymap[location] = b
    def _get_byte(self, location):
        val = self.memorymap[location]
        return val
    def _guard(self, location, write = False):
        if self.get_type_at(location) == HIGH: raise OutOfRangeException(location)
        if write and self.get_type_at(location) == STATIC: raise ReadOnlyException(location)
    def _calc_location_p(self, location):
        mult = 2
        if self.version in [4,5,6,7]: mult = 4
        if self.version == 8: mult = 8
        return location * mult
        
    def put_byte(self, location, b):
        self._guard(location, True)
        self._put_byte(location, b)
    def get_byte(self, location):
        self._guard(location)
        return self._get_byte(location)
    def get_2byte(self, location):
        self._guard(location*2)
        value = 256*self._get_byte(location*2)+self._get_byte(location*2+1)
        logging.debug('Getting 2byte %04x from location %04x' % (value, location*2))
        return value
    def get_high_byte(self, location):
        return self._get_byte(location)
    def put_2byte(self, location, b):
        self._guard(location*2, True)
        self._put_byte(location*2, b//256)
        self._put_byte(location*2+1, b%256)
    def loadp(self, location):
        location = self._calc_location_p(location)
        return self._get_byte(location)
