#!/usr/bin/python/
global  F_DEBUG
F_DEBUG = 1

def p(stringarg):
    if F_DEBUG:
        print stringarg
        pass

def getflag(): return F_DEBUG
    
