# -*- coding: utf-8 -*-
"""
对字典类型的日期支持
"""
from datetime import datetime

from daypy.utils import pretty_unit


def dict_support(option, Daypy, daypy):
    oldParse = Daypy.parse

    def parse_date(value):
        if not isinstance(value, dict):
            return

        _value = {}
        for k, v in value.items():
            _value[pretty_unit(k)] = v
        now = daypy()
        _value['year'] = _value.get('year', now.y)
        _value['month'] = _value.get('month', now.M)
        _value['day'] = _value.get('day', now.d)
        _value['hour'] = _value.get('hour', now.h)
        _value['minute'] = _value.get('minute', now.m)
        _value['second'] = _value.get('second', now.s)
        _value['microsecond'] = _value.get('microsecond', now.ms)
        return datetime(**_value)

    def parse(_, value=None, *args, **kwargs):
        dt = parse_date(value)
        return oldParse(_, dt or value, *args, **kwargs)

    Daypy.parse = parse
