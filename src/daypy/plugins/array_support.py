# -*- coding: utf-8 -*-
from datetime import datetime

from daypy.utils import get_datetime_now


def array_support(option, Daypy, daypy):
    oldParse = Daypy.parse

    def parse_date(cfg):
        date = cfg.get('date')
        utc = cfg.get('utc')
        if not isinstance(date, list):
            return date
        if len(date) <= 0:
            return get_datetime_now(utc)

        return datetime(*date)

    def parse(_, cfg):
        cfg['date'] = parse_date(cfg)
        return oldParse(_, cfg)

    Daypy.parse = parse
