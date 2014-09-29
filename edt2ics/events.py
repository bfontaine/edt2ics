#! /usr/bin/env python
# -*- coding: UTF-8 -*-


class ScheduleEvent(object):
    """
    A schedule event
    """

    def __init__(self, **kwargs):
        """
        Attributes: color, title, type_, day, tstart, tend, duration, room,
        prof.
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
