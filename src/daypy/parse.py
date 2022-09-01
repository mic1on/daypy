# -*- coding: utf-8 -*-
import itertools
import re
from datetime import datetime, date, timezone

_date_formats = (
    "%Y-%m-%d",
    "%Y%m%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%d.%m.%y",
    "%d.%m.%Y",
    "%Y %m %d",
    "%m/%d/%Y",
)

_datetime_formats = list(
    itertools.chain.from_iterable(
        [
            ["{} %H:%M:%S".format(fmt) for fmt in _date_formats],
            ["{} %H:%M".format(fmt) for fmt in _date_formats],
            ["{}T%H:%M:%S.%f%z".format(fmt) for fmt in _date_formats]
        ]
    )
)


def _parse_datetime_str(val):
    val = val.strip()
    for fmt in itertools.chain.from_iterable((_datetime_formats, _date_formats)):
        try:
            return datetime.strptime(val, fmt)
        except Exception:
            pass
    try:
        return datetime.strptime(val, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        pass


def _parse_datetime_str_regexp(val, utc=None):
    REGEX_PARSE = r"^(\d{4})[-/]?(\d{1,2})?[-/]?(\d{0,2})[Tt\s]*(\d{1,2})?:?(\d{1,2})?:?(\d{1,2})?[.:]?(\d+)?$"
    _d = re.match(REGEX_PARSE, val)
    if _d is None:
        return None
    d = [int(dd or 0) for dd in list(_d.groups())]
    if not d:
        return None
    m = d[1] or 1
    ms = int(str(d[6]).ljust(6, '0'))
    return datetime(d[0], m, d[2] or 1, d[3] or 0, d[4] or 0, d[5] or 0, ms, tzinfo=timezone.utc if utc else None)


def parse_datetime(cfg):
    date_val = cfg.get('date')
    utc = cfg.get('utc')
    if isinstance(date_val, datetime):
        return date_val
    if isinstance(date_val, date):
        return datetime.combine(date_val, datetime.min.time(), tzinfo=timezone.utc if utc else None)
    elif isinstance(date_val, str):
        _datetime = _parse_datetime_str_regexp(date_val, utc) or _parse_datetime_str(date_val)
        if not _datetime:
            raise ValueError("Error! Unable to parse `%s` as date." % date_val)
        return _datetime
    raise ValueError("Error! Unable to parse `%s` as date (unknown type)." % date_val)


if __name__ == '__main__':
    # print(parse_datetime('2019-01-01'))
    # print(parse_datetime('2022-01-01 12:00:00'))
    # print(parse_datetime('2022-01-01 11:00'))
    # print(parse_datetime('20190101 10:00'))
    # print(parse_datetime('01.01.2022 10:00:01'))
    # print(parse_datetime('01.01.23 10:00:01'))
    # print(parse_datetime('2022.03.03 10:00:01'))
    # print(parse_datetime('2019 01 01 10:00'))
    # print(parse_datetime('2019/01/01 10:00'))
    # print(parse_datetime('10/01/2022 10:00'))

    print(parse_datetime("2020-12-01T03:21:57.330Z"))
