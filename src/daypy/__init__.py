# -*- coding: utf-8 -*-
from calendar import monthrange
from datetime import datetime
from typing import Union, Callable, Optional, Any, List, Literal

import arrow
from arrow import Arrow

from daypy.utils import import_object, pretty_unit, get_plugin_names

UnitType = Optional[
    Literal[
        "year", "month", "day", "hour", "minute", "second", "microsecond",
        "y", "M", "d", "w", "h", "m", "s", "ms"
    ]
]


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

    def add(
            self,
            number: int,
            units: UnitType
    ):
        units = pretty_unit(units, plurality=True)
        dt = self.dt.shift(**{units: number})
        return daypy(dt)

    def subtract(
            self,
            number: int,
            units: UnitType
    ):
        return self.add(-number, units)

    def start_of(
            self,
            unit: UnitType = None,
            start_of: bool = True
    ):
        unit = pretty_unit(unit)

        se = datetime.min if start_of else datetime.max
        units = ["year", "month", "day", "hour", "minute", "second", "microsecond"]
        for u in units:
            if u == 'month' and not start_of:
                _date = {'year': self.y, 'month': self.M, 'day': monthrange(self.y, self.M)[1]}
            else:
                _date = {u: getattr(self.dt, u)}
            se = se.replace(**_date)
            if u == unit or unit is None:
                break
        return daypy(se)

    def end_of(
            self,
            unit: UnitType = None
    ) -> "Daypy":
        return self.start_of(unit, start_of=False)

    def is_before(
            self,
            value,
            unit: UnitType = None
    ) -> bool:
        """检查当前对象是否在指定时间之前"""
        if unit is None:
            return self < daypy(value)
        return self.end_of(unit) < daypy(value)

    def is_after(
            self,
            value,
            unit: UnitType = None
    ) -> bool:
        """检查当前对象是否在指定时间之后"""
        if unit is None:
            return self > daypy(value)
        return self.start_of(unit) > daypy(value)

    def is_same(
            self,
            value,
            unit: UnitType = None
    ):
        """检查当前对象是否与指定时间相同"""
        other = daypy(value)
        if unit is None:
            return self == other
        return self.start_of(unit) <= other <= self.end_of(unit)

    def is_between(
            self,
            start: Any,
            end: Any,
            unit: UnitType = None,
            inclusive: Optional[str] = None
    ) -> bool:
        """
        检查日期是否在指定范围日期区间
        :param start: 起始时间
        :param end: 结束时间
        :param unit: 比较单位 Union["year", "month", "day", "hour", "minute", "second", "microsecond", NoneType]
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

    def timestamp(self):
        return self.dt.timestamp()

    def value_of(self):
        return round(self.dt.timestamp() * 1000)

    def unix(self):
        return round(self.dt.timestamp())

    def get(
            self,
            unit: UnitType
    ) -> int:
        """
        返回当前对象的时间单位值。
        各个传入的单位对大小写不敏感，支持缩写和复数。
        请注意，缩写是区分大小写的。
        :param unit: 时间单位: Union["year", "month", "day", "hour", "minute", "second", "microsecond", NoneType]
        :return
        """
        return self._getter(pretty_unit(unit))

    def set(
            self,
            unit: UnitType,
            value: int
    ) -> "Daypy":
        """
        设置当前对象的时间单位值。
        各个传入的单位对大小写不敏感，支持缩写和复数。
        请注意，缩写是区分大小写的。
        调用后返回一个修改后的新实例。
        :param unit: 时间单位: Union["year", "month", "day", "hour", "minute", "second", "microsecond", NoneType]
        :param value: 时间单位值
        """
        self._setter(pretty_unit(unit), value)
        return self.clone()

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

    def __str__(self):
        return self.dt.__str__()

    def __repr__(self):
        return f"<{self.__class__.__name__} [{self.__str__()}]>"


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


def init_instance():
    def unix(timestamp: int) -> "Daypy":
        return daypy(round(timestamp * 1000))

    daypy.unix = unix


init_extend()
init_instance()
