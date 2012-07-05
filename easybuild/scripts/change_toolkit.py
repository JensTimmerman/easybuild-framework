#!/usr/bin/env python
##
# Copyright 2012 Jens Timmerman
#
# This file is part of EasyBuild,
# originally created by the HPC-UGent team.
#
# http://github.com/easybuild/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
#
##
"""
This script takes a new toolkit name and version and a list of easyconfig files.
It writes out copies of the easyconfig files but with the toolkit's changed

TODO: check for dependencies, and also change this for them
"""
import sys
def rreplace(s, old, new, occurrence=1):
    """Repalce the rightmost 'occurrence' occurrences of old with new"""
    list_ = s.rsplit(old, occurrence)
    return new.join(list_)



def main(arguments):
    """
    main function: parses arguments and calls add_header
    """
    # argument parsing
    if len(arguments) < 3 or arguments[1].endswith('.eb') or arguments[2].endswith('.eb'):
        sys.stderr.write("Usage: %s <toolkitname> <toolkit version> <filenames.eb>+ \n" % arguments[0])
        sys.exit(1)

    toolkitname = arguments[1]
    toolkitversion = arguments[2]
    files = arguments[3:]
    # TODO: use logger
    print "creating .eb file for toolkit %s-%s in %s" % (toolkitname, toolkitversion, files)

    for file_ in files:
        # get current toolkit name and value
        oldfile = open(file_)
        contents = oldfile.read()
        oldfile.close()
        # 'parse' the file
        exec(contents)
        origname = toolkit['name']
        origversion = toolkit['version']
        # create new name, only one replace here, start searching right side of the name
        newname = rreplace(file_, origname , toolkitname)
        newname = rreplace(newname, origversion, toolkitversion)
        newfile = open(newname, 'w')
        # replace old toolkit with new one
        contents = contents.replace(origname , toolkitname)
        contents = contents.replace(origversion, toolkitversion)
        # write it out
        newfile.write(contents)
        newfile.close()
        print "written out new %s" % newname


main(sys.argv)
