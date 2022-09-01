# -*- coding: utf-8 -*-
import datetime

from daypy import daypy

print(daypy('2018-04-04T16:00:00.000Z'))
print(daypy('2018-04-13 19:18:17.040+02:00'))
print(daypy('2018-04-13 19:18'))

print(daypy('2020-3-21 8:3:15').set('M', 2))