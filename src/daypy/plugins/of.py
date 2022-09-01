# -*- coding: utf-8 -*-
from datetime import timedelta, datetime


def of(option, Daypy, daypy):

    def day_of_year(this, *args, **kwargs):
        """一年中的第几天"""
        return int(this.d.strftime('%j'))

    def week_of_year(this, *args, **kwargs):
        """一年中的第几周"""
        return int(this.d.strftime('%W'))

    def day_of_week(this, *args, **kwargs):
        """一周中的第几天"""
        return int(this.d.strftime('%w'))

    Daypy.day_of_year = day_of_year
    Daypy.week_of_year = week_of_year
    Daypy.day_of_week = day_of_week


if __name__ == '__main__':
    print(timedelta(weeks=1))