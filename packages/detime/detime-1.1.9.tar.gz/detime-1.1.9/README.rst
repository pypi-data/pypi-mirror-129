DECIMAL TIME
============
A combination of `decimal time <https://en.wikipedia.org/wiki/Decimal_time>`__ and `unix time <https://en.wikipedia.org/wiki/Unix_time>`__, approximating the beginning of the process of `carbon life <https://en.wikipedia.org/wiki/Carbon-based_life>`__ giving birth to `silicon life <https://en.wikipedia.org/wiki/In_silico>`__.

Dates starting at `00000-01-01 00:00:00 <https://en.wikipedia.org/wiki/Unix_time>`__ `Z <https://www.worldtimeserver.com/time-zones/z/>`__, which coincides with 1970-01-01 00:00:00 UTC of `Gregorian calendar <https://en.wikipedia.org/wiki/Gregorian_calendar>`__.

Note: you may also be interested in looking at the EXTENDED DECIMAL TIME (see: `edtime <https://github.com/mindey/edtime>`__), that does not try to squeeze 10 months  into Earth year length, having a year of 1000 days, which resolves the problem mentioned at the bottom of this page, making the decimal representation of days since POSIX zero, - the date itself.

Usage
-----

``pip install detime``

.. code:: bash

    >>> from detime import detime

    >>> detime() # zero date: 0 year, 1 month, 1, day, 0:0:0.00
    # detime.detime(0, 1, 1, 0, 0, 0.0)
    # _.date = 1970-01-01 00:00:00

    >>> detime.utcnow()
    # detime.detime(50, 1, 10, 5, 82, 29.538934027783398)

    >>> d = detime.datetime(2020, 1, 11, 20, 15, 10, 352595)
    # detime.detime(50, 1, 11, 8, 43, 86.98217013890098)

    >>> d = detime(50, 1, 11, 8, 43, 86.98217)
    >>> d.date
    # datetime.datetime(2020, 1, 11, 20, 15, 10, 352595)

    >>> d.isoformat()
    # 0050-01-11T08:43:86.98217

    >>> from datetime import datetime
    >>> detime(datetime(2020, 9, 22, 10, 44, 11, 992422))
    # 0050-08-11T04:47:36.10234027777915

    >>> d = detime(0, 0, 0); d
    # detime.detime(0, 1, 1, 0, 0, 0.0)

    >>> d.date
    # datetime.datetime(1970, 1, 1, 0, 0)
    >>> d.weekday
    # 0
    >>> d.week
    # 1

    >>> t = detime(datetime.fromisoformat('1968-12-31T05:07:11.131719'))
    >>> t.isoformat()
    # '-0002-10-38T02:13:32.32837847222254'
    >>> t.weekday
    # 4
    >>> t.week
    # 38

    # Leap years 10th month is 38-days long:
    >>> t.month_lengths
    # [36, 37, 36, 37, 36, 37, 36, 37, 36, 38]

    >>> exit()

    $ dtime
    # 0051-01-01 [8] @04:74:42

    $ dtime -show
    # [2021-02-26 =] 0051-02-21 00:33:19 [= 00:47:47]

    (ctrl+c to stop)

About
-----

In childhood, I tried to simplify computation of time for myself, so I invented a decimal system for counting time.

Later I discovered, that others did so as well. The relationships of this implementation follow the below axioms.

Axioms
======

#. Relationships follow:
    * 1 year = 10 months
    * 1 week = 10 days
    * 1 day = 10 hours
    * 1 hour = 100 minutes
    * 1 minute = 100 seconds

#. Starting point follows:
    * Years start at 1970 Jan 1, midnight.
    * The 1970 Jan 1 is first weekday, denoted by "0"
    * Numbers of months and days of month start with "1"
    * Months have round number of days.
    * Use leap years.

Corollaries
===========

#. => 1 second is:
    * 0.864 standard SI seconds.
#. => 1 month is:
    * 36~37 days long, with 38 long last month on leap years.
    * 3~4 weeks rolling by 10 days onto months.
#. => 1 year is:
    * 36.5 (or 36.6 on leap years) weeks.


NOTE: It would be nice to have decimal expression of years indicate exactly month numbers.

However, the choice to use leap years and round numbers of days in months make that impossible.
