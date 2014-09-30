#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This module provides a class to parse schedule events from Paris Diderot's
Computer Science departement website.
"""

from bs4 import BeautifulSoup
from datetime import time, timedelta
import re
from urllib2 import urlopen
from urlparse import urljoin

from events import ScheduleEvent

HOST = 'http://localhost:2201'
PATH_FMT = '/~ufr/UFR{period}/EDT/visualiserEmploiDuTemps.php?' \
           'quoi={year},{semester}'

RE_DESC = re.compile(
    r"""
    (?P<type>[-\w]+)\s+             # COURS, TP_M2, etc
    (?P<title>.+)\s+:\s+            # course name :
    (?P<day>[a-z]+di)\s+            # {lun,mar,...}di (day)
    (?P<time>\d{1,2}h(?:\d{2})?)\s+ # 12h30
    \(dur.e\s+:\s+                  # (durée :
    (?P<duration>\dh(?:\d{2})?)\)   #  2h30)
    """,
    re.VERBOSE)
RE_ROOM = re.compile(r'^\d') # detect a room number
RE_YEAR_SUFFIX = re.compile(r'_[ML][1-3]$')

class ScheduleScraper(object):
    """
    A scraper for an HTML schedule
    """

    DAYS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']


    def __init__(self, year, semester=1, period='2014-2015', host=HOST):
        """
        - year: L3, M1 or M2
        - semester: 1 or 2
        - period: 2014-2015
        """
        path = PATH_FMT.format(year=year, semester=semester, period=period)
        self.url = urljoin(HOST, path)
        self._fetch()


    def _fetch(self):
        stream = urlopen(self.url)
        self._soup = BeautifulSoup(stream, 'lxml')


    def get_events(self):
        """
        Yield each event from the parsed page
        """
        for td in self._soup.select('td[title]'):
            desc = td.attrs.get('title')

            profs = td.select('small')
            prof = profs[0].get_text().strip() if profs else None

            for s in td.strings:
                s = s.strip()
                if RE_ROOM.match(s):
                    room = s
                    break
            else:
                room = None

            info = RE_DESC.match(desc)
            if not info:
                yield None
                continue

            tstart = self.parse_time(info.group('time'))
            h, m = self._parse_hm(info.group('duration'))
            endminutes = (tstart.hour + h) * 60 + tstart.minute + m
            tend = time(endminutes / 60, endminutes % 60)

            kw = {
                'color': td.attrs.get('bgcolor'),
                'title': info.group('title'),
                'type_': self.parse_type(info.group('type')),
                'day': self.parse_day(info.group('day')),
                'tstart': tstart,
                'tend': tend,
                'duration': timedelta(hours=h, minutes=m),
                'room': room,
                'prof': prof,
            }

            yield ScheduleEvent(**kw)


    def parse_day(self, title):
        """
        Parse a day from the page and return an integer (0 for Monday, 1 for
        Tuesday and so on).
        """
        if not title or not title in self.DAYS:
            return None
        return self.DAYS.index(title)


    def _parse_hm(self, text):
        """
        Parse a time given as '<hh>h[<mm>]' and return a tuple
        """
        t = text.split('h')
        h = int(t[0])
        m = int(t[1] or '0')
        return h, m


    def parse_time(self, title):
        """
        Parse a time and return a ``time`` object.
        """
        h, m = self._parse_hm(title)
        return time(h, m)


    def parse_type(self, type_):
        """
        Parse an event type
        """
        return re.sub(RE_YEAR_SUFFIX, '', type_.strip()).capitalize()
