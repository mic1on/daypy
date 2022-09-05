# -*- coding: utf-8 -*-
"""
对数组类型的日期支持
"""
from datetime import datetime


def array_support(option, Daypy, daypy):
    old_parse = Daypy.parse

    def parse_date(value):
        if not isinstance(value, list):
            return
        if len(value) <= 0:
            return datetime.now()

        return datetime(*value)

    def parse(_, value=None, *args, **kwargs):
        dt = parse_date(value)
        return old_parse(_, dt or value, *args, **kwargs)

    Daypy.parse = parse
