# -*- coding: utf-8 -*-
from datetime import datetime


def dict_support(option, Daypy, daypy):
    oldParse = Daypy.parse

    def parse_date(cfg):
        date = cfg.get('date')
        if not isinstance(date, dict):
            return date
        now = daypy()

        date['year'] = date.get('year', now.y)
        date['month'] = date.get('month', now.M)
        date['day'] = date.get('day', now.W)
        date['hour'] = date.get('hour', now.H)
        date['minute'] = date.get('minute', now.m)
        date['second'] = date.get('second', now.s)
        date['microsecond'] = date.get('microsecond', now.ms)
        return datetime(**date)

    def parse(_, cfg):
        cfg['date'] = parse_date(cfg)
        return oldParse(_, cfg)

    Daypy.parse = parse
