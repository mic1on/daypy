# -*- coding: utf-8 -*-
def is_leap_year(option, Daypy, daypy):
    def _is_leap_year(this) -> bool:
        return this.y % 4 == 0 and (this.y % 100 != 0 or this.y % 400 == 0)

    Daypy.is_leap_year = _is_leap_year
