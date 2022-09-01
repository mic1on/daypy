# -*- coding: utf-8 -*-
def to_array(option, Daypy, daypy):
    def _to_array(this):
        return [
            this.y,
            this.M,
            this.D,
            this.H,
            this.m,
            this.s,
            this.ms
        ]

    Daypy.to_array = _to_array
