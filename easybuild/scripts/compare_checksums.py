#!/usr/bin/env python
##
# Copyright 2014 Ghent University
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
This file compares 2 files with checksums and outputs the overlapping ones,
and the failing ones

@author Jens Timmerman
"""
import os
from vsc.utils.generaloption import SimpleOption

# options = {longopt:(help_description,type,action,default_value,shortopt),}

SimpleOption.ALLOPTSMANDATORY = False
go = SimpleOption(None, None, None, None, None)

go.log.info("Starting compare_checkups")

file1 = open(go.args[0]).readlines()
file2 = open(go.args[1]).readlines()
lines1 = dict([(line.split()[1], line.split()[0]) for line in file1])
lines2 = dict([(os.path.basename(line.split()[1]), line.split()[0]) for line in file2])

sums1 = lines1.keys()
sums2 = lines2.keys()

ok = {}
nok = []
for s in sums1:
    if os.path.basename(s) in sums2:
        if lines1[s] == lines2[os.path.basename(s)]:
            ok[s] = lines1[s]
        else:
            nok.append((s, lines1[s], lines2[os.path.basename(s)]))

for x,y in ok.iteritems():
    print y, x

for x in nok:
    print x
