# -*- coding: UTF-8 -*-

import sys
from tempfile import NamedTemporaryFile
from os import remove

try:
    import unittest2 as unittest
    from cStringIO import StringIO
except ImportError:
    from io import StringIO
    import unittest

from edt2ics.cli import write_ical, main, ScheduleScraper

def ctrlC(self, *args, **kwargs):
    raise KeyboardInterrupt


class TestCli(unittest.TestCase):

    def setUp(self):
        self.real_stdout = sys.stdout
        self.stdout = sys.stdout = StringIO()
        self.argv = sys.argv
        self.sys_exit = sys.exit
        self.exit_code = None
        self.ss_init = ScheduleScraper.__init__
        def _fake_exit(code=None):
            self.exit_code = code
        _fake_exit.__name__ = sys.exit.__name__
        sys.exit = _fake_exit

    def tearDown(self):
        sys.stdout = self.real_stdout
        sys.argv = self.argv
        sys.exit = self.sys_exit
        ScheduleScraper.__init__ = self.ss_init

    # write_ical

    def test_write_stdout(self):
        s = u'foobarXz123$$9_=+@@'

        write_ical(s, '-')

        self.stdout.seek(0)
        self.assertEquals(s, self.stdout.read())


    def test_write_file(self):
        s = u'foo&"b$**a-rXz12%x3ZZ$$9_=+@@'
        file_ = NamedTemporaryFile(delete=False)
        file_.close()
        filename = file_.name

        write_ical(s, filename)

        with open(filename, 'r') as f:
            self.assertEquals(s, f.read())

        remove(filename)


    # main

    def test_main_abort_on_interrupt(self):
        ScheduleScraper.__init__ = ctrlC
        sys.argv = ['edt2ics', 'M2']
        self.assertEquals(None, self.exit_code)
        main()
        self.assertEquals(1, self.exit_code)
