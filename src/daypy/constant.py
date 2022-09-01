# -*- coding: utf-8 -*-
from enum import Enum


class UnitEnum(Enum):
    MS = 'millisecond'
    S = 'second'
    MIN = 'minute'
    H = 'hour'
    D = 'day'
    W = 'week'
    M = 'month'
    Q = 'quarter'
    Y = 'year'
    DATE = 'date'
