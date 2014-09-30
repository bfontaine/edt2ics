#! /usr/bin/env python
# -*- coding: UTF-8 -*-

from datetime import date
from edt2ics import ScheduleScraper, iCalSchedule


def main():
    # just a test for now
    s = ScheduleScraper(year='M2', host='localhost:2201')
    ics = iCalSchedule(date(2014, 9, 29), date(2014, 12, 15))
    for ev in s.get_events():
        ics.add_event(ev)
    with open('edt.ics', 'wb') as f:
        f.write(ics.to_ical())


if __name__ == '__main__':
    main()
