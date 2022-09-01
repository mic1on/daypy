# -*- coding: utf-8 -*-
from datetime import datetime

from daypy import daypy


def test_is_daypy():
    assert daypy.is_daypy(daypy())
    assert not daypy.is_daypy(datetime)


def test_unix():
    assert daypy.unix(1318781876.721) == daypy('2011-10-17 00:17:56.721')
    assert daypy.unix(1318781876721) == daypy('2011-10-17 00:17:56.721')
    assert daypy.unix(1318781876) == daypy('2011-10-17 00:17:56')
    assert daypy.unix(0) == daypy('1970-01-01 08:00:00')

    # print(datetime.fromtimestamp(0), daypy.unix(0))
    # print(datetime.fromtimestamp(1318781876), daypy.unix(1318781876))
    # print(datetime.fromtimestamp(1318781876.721), daypy.unix(1318781876.721))
    # print(datetime.fromtimestamp(1318781876.721001), daypy.unix(1318781876.721001))
    # print(datetime.fromtimestamp(-1318781876.721001), daypy.unix(-1318781876.721001))
    # print(datetime.fromtimestamp(-1318781876), daypy.unix(-1318781876))
