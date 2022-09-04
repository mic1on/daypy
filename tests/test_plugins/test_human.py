# -*- coding: utf-8 -*-
import arrow

from daypy import daypy

daypy.extend('human', {"locale": "zh"})


def test_human():
    assert daypy.dehumanize("1小时前").format() == daypy().subtract(1, 'hour').format()