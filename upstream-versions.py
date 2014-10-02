#!/usr/bin/env python

# Retrieves X.org package versions from upstream
# and outputs a JSON data file

import re
import os
import json
import urllib2
from distutils.version import LooseVersion

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

def parse_xterm_page(category='app'):
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
        p.category = category
        p.version = m.group(3)
        p.released = m.group(1)
        p.url = os.path.join(url, filename)
        packages.setdefault(p.name, []).append(p.__dict__)

    return packages

def parse_mesa_page(category='library'):
    url = 'ftp://ftp.freedesktop.org/pub/mesa/'
    package_pattern = '\d+ (\w+ +\d+ +[\d:]+) ([\d\.]+)\s*$'
    packages = {}
    re_pkg = re.compile(package_pattern)
    for line in readurl(url).split("\n"):
        #print line
        m = re_pkg.search(line)
        if not m:
            continue
        filename = "%s-%s.%s" %('MesaLib', m.group(2), 'tar.bz2')

        p = Package('mesa')
        p.category = category
        p.version = m.group(2)
        p.released = m.group(1)
        p.url = os.path.join(url, p.version, filename)
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
        p.category = category
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
        p.category = category
        p.version = m.group(2)
        p.released = m.group(4)
        p.url = os.path.join(url, filename)
        packages.setdefault(p.name, []).append(p.__dict__)

    return packages

def parse_ffmpeg_page(category='library'):
    url = 'http://ffmpeg.org/releases/'
    package_pattern = '>(\w+)-([\.\d]+)\.(tar\.bz2)</a>\s*(\d+-\w+-\d+) (\d+:\d+)'
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
        packages.setdefault(p.name, []).append(p.__dict__)

    return packages


if __name__ == "__main__":
    import sys
    from optparse import OptionParser
    from datetime import datetime, timedelta
    from dateutil import parser as date_parser

    opt_parser = OptionParser(usage="%prog [OPTIONS] <video> [item [item...]]")
    opt_parser.add_option('-i', '--input-file', action='store', dest='input_file',
                          help="Use data from JSON file instead of querying web", default=None)
    opt_parser.add_option('-j', '--json', action='store_true', dest='json_output',
                          help="Dump all data to stdout as JSON text", default=False)
    opt_parser.add_option('-l', '--list', action='store_true', dest='list_output',
                          help="Summarize data in a textual list", default=False)
    opt_parser.add_option('-n', '--new', action='store_true', dest='new_only',
                          help="List new releases made within the past quarter", default=False)
    (options, args) = opt_parser.parse_args()

    if len(args) == 0:
        args = ['xorg', 'cairo', 'wayland', 'ffmpeg']

    data = {}
    if options.input_file is not None:
        s = open(options.input_file).read()
        data = json.loads(s)
    else:
        try:
            if 'xorg' in args:
                data.update(parse_xorg_top())
                data.update(parse_xterm_page())
                data.update(parse_mesa_page())
            if 'wayland' in args:
                data.update(parse_wayland_page())
            if 'cairo' in args:
                data.update(parse_cairo_page())
            if 'ffmpeg' in args:
                data.update(parse_ffmpeg_page())
        except:
            raise

    if options.json_output:
        print json.dumps(data, indent=4)

    elif options.list_output:
        for pkg_name in data.keys():
            for package in data[pkg_name]:
                print "%-30s %-12s %s" %(pkg_name, package['version'], package['released'])

    elif options.new_only:
        today = datetime.today()
        three_months_ago = today - timedelta(days=90)
        already_printed = {}

        print "<table>"
        for pkg_name in data.keys():
            for package in data[pkg_name]:
                # If release was this month, print it
                d = date_parser.parse(package['released'])
                # If d is None, then what?
                if d > three_months_ago:
                    released = d.strftime("%Y-%m-%d")

                    line = "<tr><td>%-30s</td> <td>%-12s</td> <td>%s</td></tr>" %(
                        pkg_name, package['version'], released)
                    if line not in already_printed:
                        print line
                        already_printed[line] = 1
        print "</table>"

    else:
        for pkg_name in data.keys():
            version = None
            for package in data[pkg_name]:
                pkg_version = LooseVersion(package['version'])

                # Compare version numbers
                if (version is None or pkg_version > version):
                    version = pkg_version
            print "%-30s %s" %(pkg_name, version)
