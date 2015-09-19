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

import mechanize

#sys.path.insert(0, os.path.realpath(
#        os.path.join(os.path.dirname(__file__), "..")))

class TwikiBrowser(object):
    def __init__(self, config):
        self.br = mechanize.Browser()
        self._url_loaded = None

        # Credentials
        self.domain = config['domain']
        self.username = config['username']
        self.team = config['team']
        self.password = config['password']

        # Basic auth
        self.br.add_password(self.domain, self.username, self.password)

    def set_debug(self, value):
        assert type(value) is bool
        self.br.set_debug_http(value)
        self.br.set_debug_redirects(value)
        self.br.set_debug_responses(value)

    def url_weekly_status(self, week):
        """Given a Week object, returns a url for the twiki status page"""
        return "%s/bin/edit/%s/%sWeek%02dStatus%d" %(
            self.domain, self.team, self.username, week.number, week.year)

    def login(self):
        self.br.form['username'] = self.username
        self.br.form['password'] = self.password
        self.br.submit()

    def get_page(self, url, relogin_if_needed=True):
        self.br.open(url)
        self._url_loaded = url

        # Select the first (index zero) form
        self.br.select_form(nr=0)
        try:
            return self.br.form['text']
        except:
            if relogin_if_needed:
                # Try logging in (adv. auth this time)
                self.login()
                self.br.response().read()
                return self.get_page(url, relogin_if_needed=False)
            else:
                print "Error editing twiki at ", url
                print dir(self.br.form)
                raise

    def set_page(self, url, text):
        if url != self._url_loaded or self.br.form is None:
            self.get_page(url)
        self.br.form['text'] = text
        self.br.submit()
        return self.br.response().read()


if __name__ == "__main__":
    config = {
        'domain': 'None',
        'username': 'None',
        'team': 'None',
        'password': 'None',
        }
    browser = TwikiBrowser(config)

    # TODO: Synthetic browser target?
