#!/usr/bin/env python

# Retrieves X.org package versions from upstream
# and outputs a JSON data file

import re
import os
import json
import urllib2

# TODO: Use beautifulsoup instead of manually parsing the page

class Package(object):
    def __init__(self, name):
        self.name = name
        self.version = None
        self.released = None
        self.category = None
        self.url = None
        self.vcs = None

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

def parse_xorg_top():
    '''Returns an array'''
    url = "http://xorg.freedesktop.org/releases/individual"
    re_page = re.compile('<a href="(\w+)/"', re.IGNORECASE)
    packages = {}
    for line in readurl(url).split("\n"):
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
    packages = {}
    re_pkg = re.compile(package_pattern)
    for line in readurl(url).split("\n"):
        m = re_pkg.search(line)
        if not m:
            continue
        filename = "%s-%s.%s" %(m.group(1), m.group(2), m.group(3))

        p = Package(m.group(1))
        p.category = category
        p.version = m.group(2)
        p.released = m.group(4)
        p.url = os.path.join(url, filename)
        p.vcs = '%s/%s/%s' %(vcs_base, category, p.name)

        # Special case to handle naming irregularities
        if p.name == 'xtrans':
            p.vcs = '%s/%s/%s' %(vcs_base, category, 'libxtrans')

        packages.setdefault(p.name, []).append(p.__dict__)

    return packages

def parse_xterm_page(category=None):
    url = 'ftp://invisible-island.net/xterm/'
    package_pattern = '\d+ (\w+ +\d+ +[\d:]+) (xterm)-(\d+)\.(tgz)'
    packages = {}
    re_pkg = re.compile(package_pattern)
    for line in readurl(url).split("\n"):
        m = re_pkg.search(line)
        if not m:
            continue
        filename = "%s-%s.%s" %(m.group(2), m.group(3), m.group(4))

        p = Package(m.group(2))
        p.version = m.group(3)
        p.released = m.group(1)
        p.url = os.path.join(url, filename)
        packages.setdefault(p.name, []).append(p.__dict__)

    return packages

def parse_wayland_page(category='wayland'):
    url = 'http://wayland.freedesktop.org/releases/'
    package_pattern = '(\w+)-([\.\d]+)\.(tar\.xz).*align="right">(\d+-\w+-\d+) (\d+:\d+)'
    packages = {}
    re_pkg = re.compile(package_pattern)
    for line in readurl(url).split("\n"):
        m = re_pkg.search(line)
        if not m:
            continue
        filename = "%s-%s.%s" %(m.group(1), m.group(2), m.group(3))

        p = Package(m.group(1))
        p.version = m.group(2)
        p.released = m.group(4)
        p.url = os.path.join(url, filename)
        packages.setdefault(p.name, []).append(p.__dict__)

    return packages

def parse_cairo_page(category='library'):
    url = 'http://www.cairographics.org/releases/'
    package_pattern = '(\w+)-([\.\d]+)\.(tar\.xz).*align="right">(\d+-\w+-\d+) (\d+:\d+)'
    packages = {}
    re_pkg = re.compile(package_pattern)
    for line in readurl(url).split("\n"):
        m = re_pkg.search(line)
        if not m:
            continue
        filename = "%s-%s.%s" %(m.group(1), m.group(2), m.group(3))

        p = Package(m.group(1))
        p.version = m.group(2)
        p.released = m.group(4)
        p.url = os.path.join(url, filename)
        packages.setdefault(p.name, []).append(p.__dict__)

    return packages


if __name__ == "__main__":
    try:
        data = {}
        data.update(parse_xorg_top())
        data.update(parse_xterm_page())
        data.update(parse_wayland_page())
        data.update(parse_cairo_page())
    except:
        raise

    data['_header'] = {
        }
    print json.dumps(data, indent=4)
