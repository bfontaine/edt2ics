#! venv/bin/python
# -*- coding: UTF-8 -*-

from edt2ics import ScheduleScraper, iCalSchedule


def main():
    # just a test for now
    s = ScheduleScraper(year='M2', host='localhost:2201')
    ics = iCalSchedule(s)
    with open('edt.ics', 'wb') as f:
        f.write(ics.to_ical())


if __name__ == '__main__':
    main()
