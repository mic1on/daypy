# -*- coding: utf-8 -*-
from enum import Enum


class UnitEnum(Enum):
    MS = 'microsecond'
    S = 'second'
    MIN = 'minute'
    H = 'hour'
    D = 'day'
    W = 'week'
    M = 'month'
    Q = 'quarter'
    Y = 'year'
    DATE = 'date'


class UnitsEnum(Enum):
    MS = 'microseconds'
    S = 'seconds'
    MIN = 'minutes'
    H = 'hours'
    D = 'days'
    W = 'weeks'
    M = 'months'
    Q = 'quarters'
    Y = 'years'
    DATE = 'dates'
