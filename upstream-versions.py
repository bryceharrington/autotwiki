#!/usr/bin/env python

# Retrieves X.org package versions from upstream
# and outputs a JSON data file

import re
import os
import json
import urllib2

# TODO: Use beautifulsoup instead of manually parsing the page

class Exit():
    """
    If an error message has already been displayed and we want to just exit the app, this
    exception is raised.
    """
    pass

def ERR(msg):
    sys.stderr.write("Error: %s\n", msg)
    sys.exit(1)

def readurl(url):
    try:
        fin = urllib2.urlopen(url)
        content = fin.read()
        fin.close()
        return content
    except urllib2.HTTPError:
        ERR("Service unavailable for %s" %(url))
        return None
    except urllib2.URLError:
        ERR("Max allowed clients? for %s" %(url))
        return None
    except:
        raise
        return None

def parse_xorg_top():
    '''Returns an array'''
    url = "http://xorg.freedesktop.org/releases/individual"
    page = readurl(url)
    if not page:
        raise Exit()

    re_page = re.compile('<a href="(\w+)/"', re.IGNORECASE)
    packages = {}
    for line in page.split("\n"):
        m = re_page.search(line)
        if not m:
            continue
        category = m.group(1)
        suburl = "%s/%s" %(url, category)
        new_pkgs = parse_xorg_page(suburl, category=category)
        packages.update(new_pkgs)

    return packages

def parse_xorg_page(url, category=None):
    '''Returns a dict of packages parsed from the given url'''
    package_pattern = '<a href="([\w-]+)-([\d\.]+)\.(tar\.\w+)">[^<]+</a></td><td align="right">([\w-]+) .*</td>'
    vcs_base = 'http://cgit.freedesktop.org/xorg'

    page = readurl(url)
    if not page:
        raise Exit()

    packages = {}
    re_pkg = re.compile(package_pattern)
    for line in page.split("\n"):
        m = re_pkg.search(line)
        if not m:
            continue
        name = m.group(1)
        version = m.group(2)
        filename = "%s-%s.%s" %(m.group(1), m.group(2), m.group(3))
        last_modified_date = m.group(4)
        pkg = {
            'name': name,
            'version': version,
            'released': last_modified_date, # Assume last modified == release date
            'category': category,
            'url': os.path.join(url, filename),
            'vcs': '%s/%s/%s' %(vcs_base, category, name)
            }

        # Special case to handle naming irregularities
        if name == 'xtrans':
            pkg['vcs'] = '%s/%s/%s' %(vcs_base, category, 'libxtrans')

        if name not in packages:
            packages[name] = []
        packages[name].append(pkg)

    return packages

def parse_xterm_page(category=None):
    url = 'ftp://invisible-island.net/xterm/'
    package_pattern = '\d+ (\w+ +\d+ +[\d:]+) (xterm)-(\d+)\.(tgz)'
    vcs_base = None

    page = readurl(url)
    if not page:
        raise Exit()

    packages = {}
    re_pkg = re.compile(package_pattern)
    for line in page.split("\n"):
        m = re_pkg.search(line)
        if not m:
            continue
        name = m.group(2)
        version = m.group(3)
        filename = "%s-%s.%s" %(m.group(2), m.group(3), m.group(4))
        last_modified_date = m.group(1)
        pkg = {
            'name': name,
            'version': m.group(3),
            'released': last_modified_date,
            'category': category,
            'url': os.path.join(url, filename),
            'vcs': None,
            }

        if name not in packages:
            packages[name] = []
        packages[name].append(pkg)

    return packages


if __name__ == "__main__":
    try:
        data = parse_xorg_top()
        #data.update(parse_xterm_page())
    except:
        sys.exit(1)

    data['_header'] = {
        }
    print json.dumps(data, indent=4)


