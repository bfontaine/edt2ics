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

from edt2ics.cli import write_ical, main

class TestCli(unittest.TestCase):

    def setUp(self):
        self.real_stdout = sys.stdout
        self.stdout = sys.stdout = StringIO()

    def tearDown(self):
        sys.stdout = self.real_stdout

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
    # TODO
