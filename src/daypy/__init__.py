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
UnitsType = Optional[
    Literal[
        "years", "months", "days", "hours", "minutes", "seconds", "microseconds", "quarters", "weeks", "weekday",
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
            units: Union[UnitType, UnitsType]
    ):
        units = pretty_unit(units, plurality=True)
        dt = self.dt.shift(**{units: number})
        return daypy(dt)

    def subtract(
            self,
            number: int,
            units: Union[UnitType, UnitsType]
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
        """?????????????????????????????????????????????"""
        if unit is None:
            return self < daypy(value)
        return self.end_of(unit) < daypy(value)

    def is_after(
            self,
            value,
            unit: UnitType = None
    ) -> bool:
        """?????????????????????????????????????????????"""
        if unit is None:
            return self > daypy(value)
        return self.start_of(unit) > daypy(value)

    def is_same(
            self,
            value,
            unit: UnitType = None
    ):
        """?????????????????????????????????????????????"""
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
        ?????????????????????????????????????????????
        :param start: ????????????
        :param end: ????????????
        :param unit: ???????????? Union["year", "month", "day", "hour", "minute", "second", "microsecond", NoneType]
        :param inclusive: ??????????????????`(`???????????? `[`????????????
               '()' ????????????????????????????????? (??????)
               '[]' ??????????????????????????????
               '[)' ??????????????????????????????????????????
        :return:

        e.g.:
        daypy("2020-11-11").is_between("2020-11-01", "2020-11-20")  // True
        daypy("1990-11-11").is_between("1990-11-11", "2020-01-01")  // False, ?????????????????????????????????
        daypy("1990-11-11").is_between("1990-11-11", "2020-01-01", None, "[)")  // True, ????????????,????????????
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
        ???????????????????????????????????????
        ?????????????????????????????????????????????????????????????????????
        ??????????????????????????????????????????
        :param unit: ????????????: Union["year", "month", "day", "hour", "minute", "second", "microsecond", NoneType]
        :return
        """
        return self._getter(pretty_unit(unit))

    def set(
            self,
            unit: UnitType,
            value: int
    ) -> "Daypy":
        """
        ???????????????????????????????????????
        ?????????????????????????????????????????????????????????????????????
        ??????????????????????????????????????????
        ?????????????????????????????????????????????
        :param unit: ????????????: Union["year", "month", "day", "hour", "minute", "second", "microsecond", NoneType]
        :param value: ???????????????
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
        # ????????????????????????????????????
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
