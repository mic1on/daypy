# -*- coding: utf-8 -*-
import arrow

from daypy import daypy

daypy.extend('dict_support')


def test_dict_support():
    assert daypy({
        "year": 1999,
        "month": 11,
        "day": 10,
        "hour": 10,
        "minute": 24,
        "second": 59
    }).format() == arrow.get('1999-11-10 10:24:59', tzinfo='local').format()
    assert daypy({
        "y": 2022,
        "M": 3,
        "d": 10,
        "h": 10,
        "m": 24,
        "s": 59
    }).format() == arrow.get('2022-3-10 10:24:59', tzinfo='local').format()
    assert daypy({
            "hour": 10,
            "minute": 24,
            "second": 59
        }).format() == arrow.get(tzinfo='local').replace(hour=10, minute=24, second=59).format()