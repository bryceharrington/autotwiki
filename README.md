autotwiki
---------

This script can be used to update your weekly status page in Twiki with
the number of git commits, bug reports filed or closed, etc.

Pre-requisites
==============

  $ sudo apt-get install python-mechanize
  $ sudo mkdir -p /var/cache/autotwiki/repositories

Usage
=====
The script assumes your status page can be edited at this URL:

  <domain>/bin/edit/<team>/<username>Week<WN>Status<Year>

The domain, team, and username settings are specified in a config file.
A sample config file is included in this package; copy it to
~/.config/autotwiki/ and modify it with your own settings.

If your status page doesn't already exist, the script will create it
using the template you point to in the "status-template" parameter in
the config file.  A sample status-template.html is included in this
package, which you can copy to ~/.config/autotwiki/ and modify to your
liking.

The script will only change the values in the Numbers section of the web
page.  Be aware that if you hand-modify these values and then re-run the
script, it will overwrite your manual changes.  However, if you delete
lines (e.g. you know you won't be reporting bugs this week, so delete
the Bugs reported line), the script will not re-add the missing line.

Also, at this point the script lacks any logic to set the numbers to
anything sensible, but presumably you have some tools to generate
whatever numbers you'd like to put there, which you can hook in at the
appropriate section of the script.  In the future perhaps we'll add a
hooks functionality to make this easier to set up.  For now, patches
welcomed...


