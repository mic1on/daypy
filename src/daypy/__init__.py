# -*- coding: utf-8 -*-
from calendar import monthrange
from typing import Union, Callable
from datetime import datetime, timezone, timedelta

from daypy.parse import parse_datetime
from daypy.utils import get_int_length, get_datetime_now, pretty_unit, import_object


def parse_date(cfg=None):
    if cfg is None:
        return datetime.now()
    date = cfg.get('date')
    utc = cfg.get('utc')
    if date is None:
        return get_datetime_now(utc)
    if isinstance(date, datetime):
        return date

    if isinstance(date, float):
        return datetime.fromtimestamp(date)
    if isinstance(date, int):
        if get_int_length(date) == 13:
            return datetime.fromtimestamp(date / 1000)
        else:
            return datetime.fromtimestamp(date)
    try:
        return parse_datetime(cfg)
    except Exception as e:
        return f'error {e}'


class DayBase(object):
    y = None
    M = None
    D = None
    W = None
    H = None
    m = None
    s = None
    ms = None


class Daypy(DayBase):

    def __init__(self, cfg=None):
        self.d: Union[datetime, None] = None
        self.parse(cfg)

    def parse(self, cfg):
        self.d = parse_date(cfg=cfg)
        self.init()

    def init(self):
        if not isinstance(self.d, datetime):
            return
        self.y = self.d.year
        self.M = self.d.month
        self.D = self.d.date()
        self.W = self.d.day
        self.H = self.d.hour
        self.m = self.d.minute
        self.s = self.d.second
        self.ms = self.d.microsecond

    def value_of(self):
        return round(self.d.timestamp() * 1000)

    def unix(self):
        return round(self.value_of() / 1000)

    def is_valid(self):
        return isinstance(self.d, datetime)

    def format(self):
        return self.d.strftime('%Y-%m-%d %H:%M:%S')

    def clone(self):
        return daypy(self.d)

    def add(self, number: int, unit: str):
        unit = pretty_unit(unit)
        self.d = self.d + timedelta(**{unit: number})
        return self

    def start_of(self,
                 unit: Union[str, None] = None,
                 start_of: bool = True
                 ) -> "Daypy":
        unit = pretty_unit(unit)

        se = datetime.min if start_of else datetime.max
        units = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
        for u in units:
            if u == 'month' and not start_of:
                _date = {'year': self.y, 'month': self.M, 'day': monthrange(self.y, self.M)[1]}
            else:
                _date = {u: getattr(self.d, u)}
            se = se.replace(**_date)
            if u == unit or unit is None:
                break
        return daypy(se)

    def is_before(self, value, unit=None) -> bool:
        """检查当前对象是否在指定时间之前"""
        return self.end_of(unit) < daypy(value)

    def is_after(self, value, unit=None) -> bool:
        """检查当前对象是否在指定时间之后"""
        return self.start_of(unit) > daypy(value)

    def is_same(self, value, unit=None):
        """检查当前对象是否与指定时间相同"""
        other = daypy(value)
        return self.start_of(unit) <= other <= self.end_of(unit)

    def end_of(self, unit: Union[str, None] = None) -> "Daypy":
        return self.start_of(unit, start_of=False)

    def get(self, unit: str) -> int:
        """
        返回当前对象的时间单位值。
        各个传入的单位对大小写不敏感，支持缩写和复数。
        请注意，缩写是区分大小写的。
        :param unit: 时间单位: year/month/day...
        :return
        """
        return self._getter(pretty_unit(unit))

    def set(self, unit: str, value: int) -> "Daypy":
        """
        设置当前对象的时间单位值。
        各个传入的单位对大小写不敏感，支持缩写和复数。
        请注意，缩写是区分大小写的。
        调用后返回一个修改后的新实例。
        :param unit: 时间单位: year/month/day...
        :param value: 时间单位值
        """
        self._setter(pretty_unit(unit), value)
        return self.clone()

    def _getter(self, attr, *args, **kwargs):
        if hasattr(self.d, attr):
            return getattr(self.d, attr)
        return None

    def _setter(self, attr, *args, **kwargs):
        if attr == 'month':
            max_day = monthrange(self.y, args[0])[1]
            real_day = max_day if self.W > max_day else self.W
            _date = {'year': self.y, 'month': args[0], 'day': real_day}
        else:
            _date = {attr: args[0]}
        self.d = self.d.replace(**_date)
        return self

    def __repr__(self):
        return f"<Daypy {self.d}>"

    def __lt__(self, other):
        return other.d > self.d

    def __gt__(self, other):
        return other.d < self.d

    def __le__(self, other):
        return other.d >= self.d

    def __ge__(self, other):
        return other.d <= self.d

    def __eq__(self, other):
        return other.d == self.d

    def __getattr__(self, attr):
        def wrapper(*args, **kwargs):
            if len(args):
                return self._setter(attr, *args, **kwargs)
            return self._getter(attr, *args, **kwargs)

        return wrapper


def daypy(date=None, *args, **kwargs):
    cfg = kwargs or {}
    cfg['date'] = date
    cfg['args'] = args
    return Daypy(cfg=cfg)


def extend(plugin: Union[str, Callable], option=None):
    if isinstance(plugin, Callable):
        plugin_func = plugin
    elif isinstance(plugin, str):
        plugin_func = import_object(f"daypy.plugins.{plugin}")
    else:
        raise TypeError(f"plugin must be str or callable, but got {type(plugin)}")
    plugin_func(option, Daypy, daypy)


def unix(timestamp):
    return daypy(timestamp)


def is_daypy(value):
    return isinstance(value, Daypy)


daypy.extend = extend
daypy.unix = unix
daypy.is_daypy = is_daypy

if __name__ == '__main__':
    daypy.extend('dict_support')
    daypy.extend('array_support')
    daypy.extend('of')
    daypy.extend('is_leap_year')

    print(daypy('2023-11-11').is_leap_year())
    # daypy.extend(to_array, {})
    print(daypy(
        {
            'hour': 16,
            'minute': 0,
            'second': 0
        }
    ))
    # # print(daypy([2010]))
    # print(daypy("some invalid string").is_valid())
    print(daypy('2022-02-20').second(30).minute(10).hour(3).format())
    print('current month', daypy().month())
    print(daypy('2022-02-20').microsecond(999))
    # print(daypy('2022-02-20').date(31))
    print(daypy().day_of_year())
    print(daypy().day_of_year(1))
    print(daypy().week_of_year())
    print(daypy('2022-10-1').day_of_week())

    print(daypy().add(-1, 'days'))

    # print(daypy().start_of('year'))
    # print(daypy().start_of('month'))
    # print(daypy().start_of('week'))
    # print(daypy().start_of('day'))
    # print("start_of_minute", daypy().start_of('minute'))
    # print("start_of_hour", daypy().start_of('hour'))
    # print("start_of_year", daypy().start_of('year'))
    #
    # print(daypy('2022-11-11 18:00:01').is_before('2022-11-11 18:00:01'))
    # print(daypy().start_of('year').format())
    # print(daypy().start_of('month').format())
    print(daypy().start_of('month').format())
    print(daypy().start_of('months').format())
    print(daypy().end_of('M').format())
    print(daypy().start_of().format())  # now
    print(daypy().start_of('day').format())
    print(daypy().end_of('day').format())
    print(daypy().is_after('2022-09-01 22:15:01', 'm'))
    print(daypy().is_same('2022-08-01 22:15:01', 'M'))
    print(daypy().is_same('2022-08-31 22:15:01', 'year'))
    print(daypy('2023-11-11').is_leap_year())
