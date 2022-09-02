# -*- coding: utf-8 -*-
from daypy import daypy

daypy.extend('is_leap_year')


def test_is_leap_year():
    assert daypy('2022-11-11').is_leap_year() == False
    assert daypy('2024-11-11').is_leap_year() == True
