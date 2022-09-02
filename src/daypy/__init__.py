# -*- coding: utf-8 -*-
from calendar import monthrange
from datetime import datetime
from typing import Union, Callable, Optional

import arrow
from arrow import Arrow

from daypy.utils import import_object, pretty_unit, pretty_units


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

    def __init__(self, *args, **kwargs):
        self.dt: Optional[Arrow] = None
        self.parse(*args, **kwargs)

    def parse(self, *args, **kwargs):
        locale = kwargs.pop('locale', 'zh')
        tz = kwargs.pop('tz', 'local')
        if args and args[0] is None:
            self.dt = arrow.get(locale=locale, tzinfo=tz)
        else:
            self.dt = arrow.get(locale=locale, tzinfo=tz, *args, **kwargs)
        self.init()

    def init(self):
        self.y = self.dt.year
        self.M = self.dt.month
        self.D = self.dt.date()
        self.W = self.dt.day
        self.H = self.dt.hour
        self.m = self.dt.minute
        self.s = self.dt.second
        self.ms = self.dt.microsecond

    def format(self, fmt: str = "YYYY-MM-DD HH:mm:ssZZ", locale: str = 'zh'):
        return self.dt.format(fmt, locale=locale)

    def clone(self):
        return daypy(self.dt)

    def add(self, number: int, units: str):
        units = pretty_units(units)
        self.dt = self.dt.shift(**{units: number})
        return self

    def subtract(self, number: int, units: str):
        return self.add(-number, units)

    def start_of(self, unit: Optional[str] = None, start_of: bool = True):
        unit = pretty_unit(unit)

        se = datetime.min if start_of else datetime.max
        units = ['year', 'month', 'day', 'hour', 'minute', 'second', 'microsecond']
        for u in units:
            if u == 'month' and not start_of:
                _date = {'year': self.y, 'month': self.M, 'day': monthrange(self.y, self.M)[1]}
            else:
                _date = {u: getattr(self.dt, u)}
            se = se.replace(**_date)
            if u == unit or unit is None:
                break
        return daypy(se)

    def end_of(self, unit: Optional[str] = None) -> "Daypy":
        return self.start_of(unit, start_of=False)

    def is_before(self, value, unit: Optional[str] = None) -> bool:
        """检查当前对象是否在指定时间之前"""
        if unit is None:
            return self < daypy(value)
        return self.end_of(unit) < daypy(value)

    def is_after(self, value, unit: Optional[str] = None) -> bool:
        """检查当前对象是否在指定时间之后"""
        if unit is None:
            return self > daypy(value)
        return self.start_of(unit) > daypy(value)

    def is_same(self, value, unit=None):
        """检查当前对象是否与指定时间相同"""
        other = daypy(value)
        if unit is None:
            return self == other
        return self.start_of(unit) <= other <= self.end_of(unit)

    def _getter(self, attr, *args, **kwargs):
        if hasattr(self.dt, attr):
            return getattr(self.dt, attr)
        return None

    def _setter(self, attr, *args, **kwargs):
        self.dt = self.dt.replace(**{attr: args[0]})
        return self

    def __lt__(self, other):
        return self.dt < other.dt

    def __le__(self, other):
        if self.dt < other.dt:
            return True
        return self.__eq__(other)

    def __gt__(self, other):
        return self.dt > other.dt

    def __ge__(self, other):
        if self.dt > other.dt:
            return True
        return self.__eq__(other)

    def __eq__(self, other):
        return self.dt == other.dt

    def __getattr__(self, attr):
        def wrapper(*args, **kwargs):
            if len(args):
                return self._setter(attr, *args, **kwargs)
            return self._getter(attr, *args, **kwargs)

        return wrapper

    def __repr__(self):
        return f'<Daypy {self.dt}>'


def extend(plugin: Union[str, Callable], option=None):
    if isinstance(plugin, Callable):
        plugin_func = plugin
    elif isinstance(plugin, str):
        plugin_func = import_object(f"daypy.plugins.{plugin}")
    else:
        raise TypeError(f"plugin must be str or callable, but got {type(plugin)}")
    plugin_func(option, Daypy, daypy)


def daypy(*args, **kwargs):
    return Daypy(*args, **kwargs)


daypy.extend = extend

if __name__ == '__main__':
    print(daypy('2022-11-11 18:00:00').is_before('2022-11-11 18:00:01'))
    print(daypy().is_before('2022-09-03 18:00:01'))
    print(daypy('2021-10-10').is_before('2022-09-03 18:00:01', 'year'))
    print(daypy('2021-10-10').is_same('2021-10-10'))

