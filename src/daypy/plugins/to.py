# -*- coding: utf-8 -*-
from typing import List, Dict


def to(option, Daypy, daypy):
    def _to_array(this) -> List:
        return [
            this.y,
            this.M,
            this.d,
            this.h,
            this.m,
            this.s,
            this.ms
        ]

    def _to_dict(this) -> Dict:
        return {
            'year': this.y,
            'month': this.M,
            'day': this.d,
            'hour': this.h,
            'minute': this.m,
            'second': this.s,
            'microsecond': this.ms,
        }

    Daypy.to_array = _to_array
    Daypy.to_dict = _to_dict
