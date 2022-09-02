# -*- coding: utf-8 -*-
from daypy.constant import UnitEnum, UnitsEnum


def import_object(name: str):
    """字符串导入模块方法"""
    if name.count(".") == 0:
        return __import__(name)
    parts = name.split(".")
    obj = __import__(".".join(parts[:-1]), fromlist=[parts[-1]])
    try:
        return getattr(obj, parts[-1])
    except AttributeError:
        raise ImportError("No module named %s" % parts[-1])


def pretty_unit(u: str):
    if u is None:
        return u
    special = {
        'M': UnitEnum.M.value,
        'y': UnitEnum.Y.value,
        'w': UnitEnum.W.value,
        'd': UnitEnum.D.value,
        'D': UnitEnum.DATE.value,
        'h': UnitEnum.H.value,
        'm': UnitEnum.MIN.value,
        's': UnitEnum.S.value,
        'ms': UnitEnum.MS.value,
        'Q': UnitEnum.Q.value
    }
    ret = special.get(u)
    if ret is not None:
        return ret
    u = u.strip().lower()
    if u.endswith('s'):
        return u[0:-1]
    return u


def pretty_units(u: str):
    if u is None:
        return u
    special = {
        'M': UnitsEnum.M.value,
        'y': UnitsEnum.Y.value,
        'w': UnitsEnum.W.value,
        'd': UnitsEnum.D.value,
        'D': UnitsEnum.DATE.value,
        'h': UnitsEnum.H.value,
        'm': UnitsEnum.MIN.value,
        's': UnitsEnum.S.value,
        'ms': UnitsEnum.MS.value,
        'Q': UnitsEnum.Q.value
    }
    ret = special.get(u)
    if ret is not None:
        return ret
    u = u.strip().lower()
    if not u.endswith('s'):
        return f"{u}s"
    return u