#!/usr/bin/env python

# Retrieves mesa changelog information for the given release

import re
import os
import sys
import json
import urllib2
from bs4 import (
    BeautifulSoup,
    Tag,
    NavigableString
    )

class Exit():
    """
    If an error message has already been displayed and we want to just exit the app, this
    exception is raised.
    """
    pass

def ERR(msg):
    if msg:
        sys.stderr.write("Error: %s\n", msg)
    sys.exit(1)

def readurl(url):
    try:
        fin = urllib2.urlopen(url)
        content = fin.read()
        fin.close()
        return content
    except urllib2.HTTPError:
        raise Exit("Service unavailable for %s" %(url))
    except urllib2.URLError:
        raise Exit("Max allowed clients? for %s" %(url))
    except:
        raise Exit()

def parse_mesa_page(mesa_version):
    '''Returns an array'''
    url = "http://mesa3d.org/relnotes/%s.html" %(mesa_version)
    data = {
        'text': ''
        }

    soup = BeautifulSoup(readurl(url))
    #data['text'] = soup.get_text()
    content = soup.find("div", attrs={"class": "content"})
    current_section = 'top'
    for child in content.children:
        if type(child) == Tag and child.name == 'h2':
            current_section = child.string
        else:
            text = str(child)
            data.setdefault(current_section, []).append(text)
        #elif type(child) == NavigableString:
        #    print "       ", child.title

        # findNextSiblings()

    return data


if __name__ == "__main__":
    from optparse import OptionParser
    from datetime import datetime, timedelta
    from dateutil import parser as date_parser

    opt_parser = OptionParser(usage="%prog [OPTIONS] <project> [project [project...]]")
    opt_parser.add_option('-j', '--json', action='store_true', dest='json_output',
                          help="Dump all data to stdout as JSON text", default=False)
    (options, args) = opt_parser.parse_args()
    if len(args) < 1:
        ERR("usage: mesa-relnotes.py <mesa-version>")

    mesa_version = args[0]
    data = parse_mesa_page(mesa_version)

    print json.dumps(data, indent=4)
