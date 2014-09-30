#! venv/bin/python
# -*- coding: UTF-8 -*-

import argparse
from edt2ics import ScheduleScraper, iCalSchedule
import sys


def write_ical(ical, output):
    if output == '-':
        sys.stdout.write(ical)
    else:
        with open(output, 'wb') as f:
            f.write(ical)


def main():
    parser = argparse.ArgumentParser(description='P7 iCal schedule generator')
    parser.add_argument('year', type=str, help='L3, M1, or M2')
    parser.add_argument('--semester', dest='semester', type=int, default=1,
            help='semester')
    parser.add_argument('--host', dest='host', type=str, default=None,
            help='remote host')
    parser.add_argument('--output', dest='output', type=str, default=None,
            help='output file')
    args = parser.parse_args()

    s = ScheduleScraper(**vars(args))
    ics = iCalSchedule(s)

    output = args.output if args.output is not None else '%s.ics' % args.year
    write_ical(ics.to_ical(), output)


if __name__ == '__main__':
    main()
