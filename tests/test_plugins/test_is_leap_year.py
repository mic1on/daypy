# -*- coding: utf-8 -*-
from daypy import daypy

daypy.extend('is_leap_year')  # noqa


def test_is_leap_year():
    assert daypy('2024').is_leap_year() == True
    assert daypy('2021-11-11').is_leap_year() == False
