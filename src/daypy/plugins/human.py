# -*- coding: utf-8 -*-
def human(option, Daypy, daypy):
    locale = option.get("locale", "zh")

    def humanize(this):
        return this.dt.humanize(locale=this.locale or locale)

    def dehumanize(input_string):
        _daypy = daypy()
        dt = _daypy.dt.dehumanize(input_string, locale=locale)
        return daypy(dt)

    Daypy.humanize = humanize
    daypy.dehumanize = dehumanize
