# -*- coding: utf-8 -*-
import arrow
from daypy import daypy


def test_daypy():
    assert daypy().format() == arrow.now().format()
    assert daypy('2022-09-02 09:38:51').format() == arrow.get('2022-09-02 09:38:51', tzinfo='local').to('local').format()
    assert daypy('2022-09-02 09:38:52', locale='en-us', tz='utc').format() == arrow.get('2022-09-02 09:38:52', locale='en-us').format()
    assert daypy('2022-09-02 09:38:53', locale='en-us', tz='utc').format() == arrow.get('2022-09-02 09:38:53', locale='en-us').format()
    assert daypy(1662083462).format() == arrow.get(1662083462).to('local').format()
    assert daypy(1662083462123).format() == arrow.get(1662083462123).to('local').format()

    # add and subtract
    assert daypy('2022-12-31 15:37:30').add(-10, 'M').format() == arrow.get('2022-12-31 15:37:30', tzinfo='local').shift(months=-10).format()
    assert daypy('2011-12-31 15:37:30').add(1, 'y').format() == arrow.get('2011-12-31 15:37:30', tzinfo='local').shift(years=1).format()

    assert daypy('2022-12-31 15:37:30').subtract(12, 'months').format() == arrow.get('2022-12-31 15:37:30', tzinfo='local').shift(months=-12).format()

    # start of and end of
    assert daypy('2022-12-31').start_of().format() == arrow.get('2022-01-01 00:00:00', tzinfo='local').format()
    assert daypy('2022-12-31').start_of('year').format() == arrow.get('2022-01-01 00:00:00', tzinfo='local').format()
    assert daypy('2022-12-31').start_of('M').format() == arrow.get('2022-12-01 00:00:00', tzinfo='local').format()
    assert daypy('2022-12-31').start_of('day').format() == arrow.get('2022-12-31 00:00:00', tzinfo='local').format()
    assert daypy('2022-12-11').end_of('M').format() == arrow.get('2022-12-31 23:59:59', tzinfo='local').format()
    assert daypy('2022-12-11').end_of('day').format() == arrow.get('2022-12-11 23:59:59', tzinfo='local').format()