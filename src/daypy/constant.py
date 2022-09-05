# -*- coding: utf-8 -*-
from dataclasses import dataclass, asdict, field


@dataclass(frozen=True)
class Units:
    y: str = field(default='year')
    M: str = field(default='month')
    d: str = field(default='day')
    h: str = field(default='hour')
    m: str = field(default='minute')
    s: str = field(default='second')
    ms: str = field(default='microsecond')
    Q: str = field(default='quarter')
    W: str = field(default='week')
    D: str = field(default='date')

    @classmethod
    def to_dict(cls, plurality=False):
        _dict = asdict(cls())
        if plurality:
            for k, v in _dict.items():
                _dict[k] = f'{v}s'
        return _dict
