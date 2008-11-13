#!/usr/bin/env python

# Copyright 2008 - Michael Brunton-Spall
# This defines the ztext and zcharacter schemes

import logging
class ztext:
    def __init__(self, memory):
        self.memory = memory
    def get_text_at(self, location):
        text = []
        word = 0
        while (word & 0x8000) == 0:
            word = self.memory.get_2byte(location)
            location += 1
            text += [(word&0x7c00)>>10, (word&0x03e0)>>5, word&0x001f]
        return text

def to_zscii(zchars):
    alphabet = 'a'
    output = ""
    for zch in zchars:
        if zch > 5:
            output += chr(ord(alphabet)+zch -6)
            alphabet = 'a'
        else:
            if zch == 4:
                alphabet = 'A'
    return output
