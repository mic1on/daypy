# -*- coding: utf-8 -*-
from calendar import monthrange
from datetime import datetime
from typing import Union, Callable, Optional, Any, List

import arrow
from arrow import Arrow

from daypy.utils import import_object, pretty_unit, get_plugin_names


class Daypy(object):

    def __init__(self, *args, **kwargs):
        self.dt: Optional[Arrow] = None
        self.locale = kwargs.pop('locale', 'zh')
        self.tz = kwargs.pop('tz', 'local')
        self.short_attrs = ['y', 'M', 'd', 'w', 'h', 'm', 's', 'ms']
        self.parse(*args, **kwargs)

    def parse(self, *args, **kwargs):

        if args:
            arg = args[0]
            if isinstance(arg, Daypy):
                self.dt = arrow.get(arg.dt, locale=self.locale, tzinfo=self.tz)
            if arg is None:
                self.dt = arrow.get(locale=self.locale, tzinfo=self.tz)

        if not self.dt:
            self.dt = arrow.get(locale=self.locale, tzinfo=self.tz, *args, **kwargs)

    def format(self, fmt: str = "YYYY-MM-DD HH:mm:ssZZ", locale: str = 'zh'):
        return self.dt.format(fmt, locale=locale)

    def clone(self):
        return daypy(self.dt)

    def add(self, number: int, units: str):
        units = pretty_unit(units, plurality=True)
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

    def is_between(self,
                   start: Any,
                   end: Any,
                   unit: Optional[str] = None,
                   inclusive: Optional[str] = None) -> bool:
        """
        检查日期是否在指定范围日期区间
        :param start: 起始时间
        :param end: 结束时间
        :param unit: 比较单位
        :param inclusive: 区间表达式：`(`表示排除 `[`表示包含
               '()' 不包含开始和结束的日期 (默认)
               '[]' 包含开始和结束的日期
               '[)' 包含开始日期但不包含结束日期
        :return:

        e.g.:
        daypy("2020-11-11").is_between("2020-11-01", "2020-11-20")  // True
        daypy("1990-11-11").is_between("1990-11-11", "2020-01-01")  // False, 默认排除起始和结束时间
        daypy("1990-11-11").is_between("1990-11-11", "2020-01-01", None, "[)")  // True, 包含起始,排除结束
        """

        inclusive = inclusive or "()"
        exclude_start = inclusive[0] == "("
        exclude_end = inclusive[1] == ")"
        return (
                       (self.is_after(start, unit) if exclude_start else not self.is_before(start, unit))
                       and
                       (self.is_before(end, unit) if exclude_end else not self.is_after(end, unit))
               ) or (
                       (self.is_before(start, unit) if exclude_start else not self.is_after(start, unit))
                       and
                       (self.is_after(end, unit) if exclude_end else not self.is_before(end, unit))
               )

    def value_of(self):
        return round(self.dt.timestamp() * 1000)

    def unix(self):
        return round(self.value_of() / 1000)

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

    def __getattr__(self, attr: str):
        # 特殊简写属性返回对应的值
        if attr in self.short_attrs:
            return getattr(self.dt, pretty_unit(attr))

        def wrapper(*args, **kwargs):
            if len(args):
                return self._setter(attr, *args, **kwargs)
            return self._getter(attr, *args, **kwargs)

        return wrapper

    def __repr__(self):
        return f'<Daypy {self.dt}>'


def daypy(*args, **kwargs) -> "Daypy":
    return Daypy(*args, **kwargs)


def init_extend():
    def extend(plugin: Union[str, Callable, List[Union[str, Callable]]],
               option: Optional[dict] = None):
        if option is None:
            option = {}
        if isinstance(plugin, Callable):
            plugin_func = plugin
        elif isinstance(plugin, str):
            plugin_func = import_object(f"daypy.plugins.{plugin}.{plugin}")
        elif isinstance(plugin, list):
            [extend(pg, {}) for pg in plugin]
            return
        else:
            raise TypeError(f"plugin must be str/callable/list, but got {type(plugin)}")
        plugin_func(option, Daypy, daypy)

    def extends():
        return get_plugin_names()

    daypy.extend = extend
    daypy.extends = extends


init_extend()
