#! /usr/bin/env python
# -*- coding: UTF-8 -*-

"""
This module provides a class to parse schedule events from Paris Diderot's
Computer Science departement website.
"""

from bs4 import BeautifulSoup
from urllib2 import urlopen
from urlparse import urljoin

HOST = 'http://localhost:2201'
PATH_FMT = '/~ufr/UFR2014-2015/EDT/visualiserEmploiDuTemps.php?' \
           'quoi={year},{semester}'


class ScheduleScraper(object):
    """
    A scraper for an HTML schedule
    """

    def __init__(self, year, semester=1, host=HOST):
        """
        - year: L3, M1 or M2
        - semester: 1 or 2
        """
        path = PATH_FMT.format(year=year, semester=semester)
        self.url = urljoin(HOST, path)
        html = urlopen(self.url).read()
        self._soup = BeautifulSoup(html, 'lxml')


    def get_events(self):
        """
        Yield each event from the parsed page
        """
        tds = self._soup.select('td')
        # TODO
