# -*- coding: utf-8 -*-
from datetime import datetime
import pytest
from daypy import daypy


@pytest.fixture
def now():
    return datetime.now()


class TestGetter:

    def test_year(self, now):
        assert daypy().get('year') == now.year
        assert daypy().get('years') == now.year
        assert daypy().get('y') == now.year
        assert daypy().year() == now.year
        assert daypy().year(2000).year() == 2000

    def test_month(self, now):
        assert daypy().get('month') == now.month
        assert daypy().get('months') == now.month
        assert daypy().get('M') == now.month
        assert daypy().month() == now.month
        assert daypy().month(10).month() == 10

    def test_day(self, now):
        assert daypy().get('day') == now.day
        assert daypy().get('days') == now.day
        assert daypy().get('d') == now.day
        assert daypy().day() == now.day
        assert daypy().day(5).day() == 5


class TestSetter:

    def test_year(self):
        assert daypy().set('year', 2000).year() == 2000
        assert daypy().set('years', 1994).year() == 1994
        assert daypy().set('y', 1988).year() == 1988
