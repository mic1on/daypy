# -*- coding: utf-8 -*-
import datetime

import arrow
from daypy import daypy


def test_daypy():
    assert daypy().format() == arrow.now().format()
    assert daypy('2022-09-02 09:38:51').format() == arrow.get('2022-09-02 09:38:51', tzinfo='local').to(
        'local').format()
    assert daypy('2022-09-02 09:38:52', locale='en-us', tz='utc').format() == arrow.get('2022-09-02 09:38:52',
                                                                                        locale='en-us').format()
    assert daypy('2022-09-02 09:38:53', locale='en-us', tz='utc').format() == arrow.get('2022-09-02 09:38:53',
                                                                                        locale='en-us').format()
    assert daypy(1662083462).format() == arrow.get(1662083462).to('local').format()
    assert daypy(1662083462123).format() == arrow.get(1662083462123).to('local').format()

    # add and subtract
    assert daypy('2022-12-31 15:37:30').add(-10, 'M').format() == arrow.get('2022-12-31 15:37:30',
                                                                            tzinfo='local').shift(months=-10).format()
    assert daypy('2011-12-31 15:37:30').add(1, 'y').format() == arrow.get('2011-12-31 15:37:30', tzinfo='local').shift(
        years=1).format()

    assert daypy('2022-12-31 15:37:30').subtract(12, 'months').format() == arrow.get('2022-12-31 15:37:30',
                                                                                     tzinfo='local').shift(
        months=-12).format()

    # start of and end of
    assert daypy('2022-12-31').start_of().format() == arrow.get('2022-01-01 00:00:00', tzinfo='local').format()
    assert daypy('2022-12-31').start_of('year').format() == arrow.get('2022-01-01 00:00:00', tzinfo='local').format()
    assert daypy('2022-12-31').start_of('M').format() == arrow.get('2022-12-01 00:00:00', tzinfo='local').format()
    assert daypy('2022-12-31').start_of('day').format() == arrow.get('2022-12-31 00:00:00', tzinfo='local').format()
    assert daypy('2022-12-11').end_of('M').format() == arrow.get('2022-12-31 23:59:59', tzinfo='local').format()
    assert daypy('2022-12-11').end_of('day').format() == arrow.get('2022-12-11 23:59:59', tzinfo='local').format()

    assert daypy('2019-01-25').add(1, 'day').subtract(1, 'year').year(2009).unix() == 1232899200

    # is before and is after
    assert not daypy('2022-11-11').is_before('2022-11-11')
    assert daypy('2021-01-09').is_before('2021-11-11')
    assert daypy('2021-01-09').is_after('2020-11-11')
    assert daypy('2021-01-09').is_same('2021-01-09')
    now = datetime.datetime.now()
    assert daypy(now).is_same(now)
    assert daypy(
        '1994-04-21'
    ).add(1, 'M').add(2, 'year').subtract(1, 'day').is_same(
        '1996-05-20'
    )

    # is between
    assert daypy("2020-11-11").is_between("2020-11-01", "2020-11-20")
    assert not daypy("1990-11-11").is_between("1990-11-11", "2020-01-01")
    assert daypy("1990-11-11").is_between("1990-11-11", "2020-01-01", None, "[)")