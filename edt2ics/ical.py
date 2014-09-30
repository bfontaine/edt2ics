#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import datetime
from icalendar import Calendar, Event, vRecur
from uuid import uuid4


class iCalSchedule(object):

    DAYS = ['MO', 'TU', 'WE', 'TH', 'FR', 'SA', 'SU']

    def __init__(self, startdate, enddate):
        self.startdate = startdate
        self.enddate = enddate
        self._first_weekdays = {} # cache
        self._init_ical()


    def _init_ical(self):
        cal = Calendar()
        cal.add('version', '2.0')
        cal.add('prodid', '-//edt2ics//bfontaine.net//')
        self.cal = cal


    def _recur_params(self, wday):
        return {
            'freq': 'weekly',
            'wkst': self.DAYS[0],
            'byday': self.DAYS[wday],
            'until': self.enddate,
        }


    def add_event(self, ev):
        dtstart = datetime.combine(self.startdate, ev.tstart)
        dtend = datetime.combine(self.startdate, ev.tend)

        iev = Event()
        iev.add('uid', str(uuid4()))
        iev.add('dtstart', dtstart)
        iev.add('dtend', dtend)
        iev.add('rrule', vRecur(self._recur_params(ev.day)))
        iev.add('summary', '%s %s' % (ev.type_, ev.title))
        iev.add('location', ev.room)
        iev.add('description', ev.prof)
        self.cal.add_component(iev)


    def to_ical(self):
        return self.cal.to_ical()
