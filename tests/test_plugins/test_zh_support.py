# -*- coding: utf-8 -*-
import arrow

from daypy import daypy

daypy.extend('zh_support')


def test_zh_support():
    assert daypy('1999年12月31日23点59分59秒').format() == arrow.get('1999-12-31 23:59:59', tzinfo='local').format()
    assert daypy('2003年5月8日').format() == arrow.get('2003-05-08', tzinfo='local').format()
    assert daypy('2003年5月').format() == arrow.get('2003-05-01', tzinfo='local').format()
    assert daypy('03年5月').format() == arrow.get('2003-05-01', tzinfo='local').format()
    assert daypy('12年12月3日23点59分59秒').format() == arrow.get('2012-12-03 23:59:59', tzinfo='local').format()
    assert daypy('12/02/2022').format() == arrow.get('2022-12-02', tzinfo='local').format()
