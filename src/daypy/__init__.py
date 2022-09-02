# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Union, Callable, Optional

import arrow
from arrow import Arrow

from daypy.utils import import_object


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
        tz = kwargs.pop('tz', 'local')
        if args and args[0] is None:
            self.dt = arrow.get().to(tz)
        else:
            self.dt = arrow.get(*args, **kwargs).to(tz)
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
    print(arrow.get().to('local'))
    print(arrow.now())
    print(arrow.utcnow())
    daypy.extend('dict_support')
    daypy()
    print(daypy(
        {
            "year": 1999,
            "month": 11,
            "day": 10
        }
    ).format())
    print(daypy(datetime.now()).format())
    print(daypy('2018-04-04T16:00:00.000Z'))
    print(daypy('2018-04-13 19:18:17.040+02:00'))
    print(daypy('2018-04-13 19:18'))
    print(daypy("12-25-1995", "MM-DD-YYYY"))
    print(daypy('1970-01-01', 'YYYY-MM-DD'))
    print(daypy(1318781876406).format())
