# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 19:18:32 2024

@author: Lim Jing
"""


from enum import Enum
from functools import reduce
from numpy import ma
import operator


class EventMsgType(Enum):
    FIELD_GOAL_MADE = 1
    FIELD_GOAL_MISSED = 2
    FREE_THROW_ATTEMPT = 3
    REBOUND = 4
    TURNOVER = 5
    FOUL = 6
    VIOLATION = 7
    SUBSTITUTION = 8
    TIMEOUT = 9
    JUMP_BALL = 10
    EJECTION = 11
    PERIOD_BEGIN = 12
    PERIOD_END = 13
    INSTANT_REPLAY = 18



class Player():
    def __init__(self, name, shirt_num):
        self.name = name
        self.shirt_num = shirt_num
        self.on = []

    def __lt__(self, other):
        return self.shirt_num < other.shirt_num

    def add_on_off(self, on, off):
        self.on.append((on, off))

    def create_mask(self, x):
        try:
            mask = ma.masked_where(~(reduce(operator.or_,[(x>=on) & (x<=off) for (on,off) in self.on])), x)
        except TypeError:
            mask = ma.masked_where(x>0, x)
        return mask
