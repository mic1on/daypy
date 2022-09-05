# -*- coding: utf-8 -*-
import os
from typing import List, Callable

from daypy.constant import Units


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


def pretty_unit(u: str, plurality: bool = False):
    if u is None:
        return u
    ret = Units.to_dict(plurality).get(u)
    if ret is not None:
        return ret
    u = u.strip().lower()
    if not plurality:
        if u.endswith('s'):
            return u[0:-1]
    else:
        if not u.endswith('s'):
            return f"{u}s"
    return u


def get_modules(package_path="."):
    modules = []
    files = os.listdir(package_path)

    for file in files:
        if not file.startswith("__"):
            name, ext = os.path.splitext(file)
            modules.append(name)

    return modules


def get_plugin_names() -> List[str]:
    from daypy import plugins
    return get_modules(plugins.__path__[0])


def get_plugin_modules() -> List[Callable]:
    return [import_object(f'daypy.plugins.{name}.{name}') for name in get_plugin_names()]
