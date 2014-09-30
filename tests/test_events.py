# -*- coding: UTF-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from edt2ics.events import ScheduleEvent

class TestEvents(unittest.TestCase):

    # __init__

    def test_init_with_nonstandard_attributes(self):
        attrs = {
            'an_int': 42,
            'a_bool': True,
            'an_str': "foo",
        }
        event = ScheduleEvent(**attrs)

        self.assertEquals(attrs['an_int'], event.an_int)
        self.assertEquals(attrs['a_bool'], event.a_bool)
        self.assertEquals(attrs['an_str'], event.an_str)

