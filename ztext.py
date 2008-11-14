#!/usr/bin/env python

# Copyright 2008 - Michael Brunton-Spall
# This defines the ztext and zcharacter schemes

import logging

alphabet1 = "\n     abcdefghijklmnopqrstuvwxyz"
alphabet2 = "\n     ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet3 = "\n      \n0123456789.,!?_#'\"/\\-:()"


def get_text_at(memory, location):
    text = []
    word = 0
    while (word & 0x8000) == 0:
        word = memory.get_2byte(location)
        location += 1
        text += [(word&0x7c00)>>10, (word&0x03e0)>>5, word&0x001f]
    return text

def to_zscii(zchars):
    alphabet = alphabet1
    output = ""
    for zch in zchars:
        if zch > 5:
            output += alphabet[zch]
            alphabet = alphabet1
        else:
            if zch == 4:
                alphabet = alphabet2
            if zch == 5:
                alphabet = alphabet3
            if zch == 0:
                output += " "
            if zch == 1:
                output += "\n"
    return output

def zchar_from_int(alphabet, char):
    return alphabet.find(char)
    #return ord(char)-ord(alphabet)+6

def from_zscii(text):
    output = []
    for ch in text:
        if ch.isupper():
            output.append(4)
            output.append(zchar_from_int(alphabet2, ch))
        elif ch in alphabet3:
            output.append(5)
            output.append(zchar_from_int(alphabet3, ch))            
        else:
            output.append(zchar_from_int(alphabet1, ch))
    append = 0
    if (len(output) % 3) != 0:
        append = (len(output) % 3)+1
    if len(output) == 0:
        append = 3
        
    for x in range(append):
        output.append(4)
    return output

def to_bytes_from_triple(zchars, last= False):
    output = 0x0000
    if last:
        output = 0x8000
    result = output | zchars[0] << 10 | zchars[1] << 5 | zchars[2]
    return [(result & 0xFF00) >> 8, result & 0xFF]   
def to_bytes(zchars):
    bytes = []
    while (len(zchars) >= 3):
        if len(zchars) == 3:
            bytes += to_bytes_from_triple(zchars[0:3], True)
        else:
            bytes += to_bytes_from_triple(zchars[0:3])
        zchars = zchars[3:]
    #bytes[-1] |= 0x80
    return bytes
    