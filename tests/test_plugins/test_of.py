# -*- coding: utf-8 -*-
from datetime import datetime

from daypy import daypy

daypy.extend('of')  # noqa


class TestOfGet:

    def test_day_of_year(self):
        assert daypy('2024').day_of_year() == 1
        assert daypy('2021-11-12').day_of_year() == 316
        assert daypy('2022-09-01').end_of('month').day_of_year() == 273
        assert daypy().day_of_year() == int(datetime.now().strftime('%j'))

    def test_week_of_year(self):
        assert daypy('2021-11-12').week_of_year() == 45
        assert daypy('2022').week_of_year() == 0
        assert daypy('2022-09-01').end_of('month').week_of_year()