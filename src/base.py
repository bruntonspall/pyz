#!/usr/bin/env python

# Copyright 2008 - Michael Brunton-Spall
# This defines base classes, like numbers, variables etc.

import logging
class number:
    def __init__(self, bytepair):
        self.value = bytepair % 0x10000
    def _signed_value(self):
        if self.value <= 0x7fff:
            return self.value
        else:
            return self.value-0x10000
    def __eq__(self, other):
        return self._signed_value() == other
    def __int__(self):
        return self._signed_value()
    def __add__(self, other):
        return number(self._signed_value() + int(other))
    def __sub__(self, other):
        return number(self._signed_value() - int(other))
    def __div__(self, other):
        return number(self._signed_value() // int(other))
    def __mul__(self, other):
        return number(self._signed_value() * int(other))
    def __mod__(self, other):
        return number(self._signed_value() % int(other))
    def __or__(self, other):
        return number(self._signed_value() | int(other))
    def __and__(self, other):
        return number(self._signed_value() & int(other))
    def __invert__(self):
        return number(~self._signed_value())
    def __index__(self):
        return self._signed_value()
        
    def __repr__(self):
        return "0x%04x (%d)" % (self.value, self._signed_value())
    def __str__(self):
        return "%d" % (self._signed_value())
    def as_signed(self):
        if self.value <= 0x7fff:
            return number(self.value)
        else:
            return number(self.value-0xFFFF-1)

def hex(val):
    return "0x%02x" % (val)
def to_hexlist(obj):
    s = ""
    for x in obj:
        s += hex(x) + " " 
    return s