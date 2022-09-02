# -*- coding: utf-8 -*-
from copy import deepcopy
from datetime import datetime


def dict_support(option, Daypy, daypy):
    oldParse = Daypy.parse

    def parse_date(value):
        if not isinstance(value, dict):
            return

        _value = deepcopy(value)
        now = daypy()
        print("now", now)
        _value['year'] = _value.get('year', now.y)
        _value['month'] = _value.get('month', now.M)
        _value['day'] = _value.get('day', now.W)
        _value['hour'] = _value.get('hour', now.H)
        _value['minute'] = _value.get('minute', now.m)
        _value['second'] = _value.get('second', now.s)
        _value['microsecond'] = _value.get('microsecond', now.ms)
        return datetime(**_value)

    def parse(_, value=None, *args, **kwargs):
        dt = parse_date(value)
        return oldParse(_, dt or value, *args, **kwargs)

    Daypy.parse = parse
