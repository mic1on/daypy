# -*- coding: utf-8 -*-
"""
对中文日期的支持
"""
import itertools
from datetime import datetime

_date_formats = (
    "%Y年%m月%d日", "%y年%m月%d日",
    "%Y年%m月", "%y年%m月",
    "%m月%d日", "%m月%d号",
    "%Y%m%d",
    "%Y/%m/%d",
    "%Y.%m.%d",
    "%d.%m.%y",
    "%d.%m.%Y",
    "%Y %m %d",
    "%m/%d/%Y"
)

_datetime_formats = list(
    itertools.chain.from_iterable(
        [
            ["{} %H:%M:%S".format(fmt) for fmt in _date_formats],
            ["{} %H:%M".format(fmt) for fmt in _date_formats],
            ["{}%H点%M分%S秒".format(fmt) for fmt in _date_formats]
        ]
    )
)


def _parse_datetime_str(val):
    val = val.strip()
    for fmt in itertools.chain.from_iterable((_datetime_formats, _date_formats)):
        try:
            ok = datetime.strptime(val, fmt)
            return ok
        except Exception:
            pass
    try:
        return datetime.strptime(val, "%Y-%m-%d %H:%M:%S.%f")
    except Exception:
        pass


def zh_support(option, Daypy, daypy):
    old_parse = Daypy.parse

    def parse_date(value, *args, **kwargs):
        # 如果存在第二参数，且第一参数不是字符串，不解析
        if len(args) > 0 or not isinstance(value, str):
            return value

        return _parse_datetime_str(value)

    def parse(_, value=None, *args, **kwargs):
        dt = parse_date(value, *args, **kwargs)
        return old_parse(_, dt or value, *args, **kwargs)

    Daypy.parse = parse
