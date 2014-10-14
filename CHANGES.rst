v0.1.2 (next version)
---------------------

- ``DTEND`` property fixes (was one day too early — #3)
- ``ScheduleScraper#get_events`` fixed for Python 3 (the time parsing was
  failing due to ``/`` giving floats instead of ints)
- The command-line application exits with ``1`` on keyboard interrupt


v0.1.1 (current version)
------------------------

- first public release
