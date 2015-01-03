#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 Samsung Electronics, Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import (date, datetime, timedelta)

class Week(object):
    STARTS_ON_SUNDAY = False

    def __init__(self, week_number=None, year=None):
        d = datetime.now()
        if week_number is not None:
            if year is None:
                year = d.year
            assert type(week_number) is int
            assert type(year) is int

            # Calculate the first day in the given week
            fmt = '%Y-%U-%w' if Week.STARTS_ON_SUNDAY else '%Y-%W-%w'
            d = datetime.strptime('%04d-%02d-1' %(year, week_number), fmt)
            if date(year, 1, 4).isoweekday() > 4:
                d -= timedelta(days=7)

        self.date_in_week = datetime.date(d)

    @property
    def begin(self):
        """Returns a date object for the first day of the week"""
        weekday = self.date_in_week.isoweekday() % 7
        begin = self.date_in_week - timedelta(days=weekday)
        assert begin.isoweekday() == 7 # Sunday
        return begin

    @property
    def end(self):
        """Returns date object for the last day of the week"""
        end = self.begin + timedelta(days=6)
        assert end.isoweekday() == 6
        return end

    @property
    def number(self):
        """Returns the week number of the date"""
        return self.date_in_week.isocalendar()[1]

    @property
    def year(self):
        """Returns the year from the end of the week"""
        return self.end.year

    def description(self):
        """Return a description of the calendar week (Sunday to Saturday)
        containing the date d, avoiding repetition.

        >>> from datetime import date
        >>> Week(date(2013, 12, 30)).description()
        'Dec 29, 2013 - Jan 4, 2014'
        >>> Week(date(2014, 1, 25)).description()
        'Jan 19 - 25, 2014'
        >>> Week(date(2014, 1, 26)).description()
        'Jan 26 - Feb 1, 2014'
        """
        assert self.begin <= self.date_in_week <= self.end

        if self.begin.year != self.end.year:
            fmt = '{0:%b} {0.day}, {0.year} - {1:%b} {1.day}, {1.year}'
        elif self.begin.month != self.end.month:
            fmt = "{0:%b} {0.day} - {1:%b} {1.day}, {1.year}"
        else:
            fmt = "{0:%b} {0.day} - {1.day}, {1.year}"

        return fmt.format(self.begin, self.end)

if __name__ == "__main__":
    week = Week(52, 2014)

    print "Description:    ", week.description()
    print "Week beginning: ", week.begin
    print "Week ending:    ", week.end
    print "Week number:    ", week.number
    print "Year:           ", week.year
