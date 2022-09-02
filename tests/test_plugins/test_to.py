# -*- coding: utf-8 -*-
from daypy import daypy

daypy.extend('to')


def test_to():
    # to array
    assert daypy('2020-11-12').to_array() == [2020, 11, 12, 0, 0, 0, 0]
    # to dict
    assert daypy('2022-11-12 10:10:20').to_dict() == {'year': 2022,
                                                      'day': 12,
                                                      'hour': 10,
                                                      'microsecond': 0,
                                                      'minute': 10,
                                                      'month': 11,
                                                      'second': 20}
