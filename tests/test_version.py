# -*- coding: UTF-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from edt2ics import __version__

class TestVersion(unittest.TestCase):

    def test_version_format(self):
        self.assertRegexpMatches(__version__, r'^\d+\.\d+\.\d+')

