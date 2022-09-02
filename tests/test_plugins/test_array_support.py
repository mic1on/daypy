# -*- coding: utf-8 -*-
import arrow

from daypy import daypy

daypy.extend('array_support')


def test_dict_support():
    assert daypy(
        [2021, 10, 10, 15, 10, 30, 155]
    ).format() == arrow.get('2021-10-10 15:10:30.155', tzinfo='local').format()
    assert daypy(
        [2022, 1, 1, 3, 3, 3]
    ).format() == arrow.get('2022-01-01 03:03:03', tzinfo='local').format()
