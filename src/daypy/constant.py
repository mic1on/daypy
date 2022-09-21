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
    D: str = field(default='date', metadata={'plurality': False})
    WD: str = field(default='weekday', metadata={'plurality': False})

    @classmethod
    def to_dict(cls, plurality=False):
        _dict = asdict(cls())

        for k, v in _dict.items():
            field_plurality = cls.__dataclass_fields__[k].metadata.get('plurality')  # type: ignore
            _plurality = plurality if field_plurality is None else field_plurality
            if _plurality:
                _dict[k] = f'{v}s'
        return _dict

    @classmethod
    def to_plural(cls, unit):
        return unit if unit in cls.to_dict(plurality=True).values() else f"{unit}s"

    @classmethod
    def to_singular(cls, unit):
        return unit if unit in cls.to_dict(plurality=False).values() else unit[:-1]