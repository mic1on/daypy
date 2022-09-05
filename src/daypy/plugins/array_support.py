# -*- coding: utf-8 -*-
"""
对数组类型的日期支持
"""
from datetime import datetime


def array_support(option, Daypy, daypy):
    oldParse = Daypy.parse

    def parse_date(value):
        if not isinstance(value, list):
            return
        if len(value) <= 0:
            return

        return datetime(*value)

    def parse(_, value=None, *args, **kwargs):
        dt = parse_date(value)
        return oldParse(_, dt or value, *args, **kwargs)

    Daypy.parse = parse
