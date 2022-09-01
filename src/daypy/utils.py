# -*- coding: utf-8 -*-
from datetime import datetime, timezone

from daypy.constant import UnitEnum


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


def get_int_length(num: int):
    """获取整数的长度"""
    if not isinstance(num, int):
        raise ValueError("num must be int")
    return str(num).__len__()


def get_datetime_now(utc=None):
    return datetime.now() if not utc else datetime.utcnow()


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
