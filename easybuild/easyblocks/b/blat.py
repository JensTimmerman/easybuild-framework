##
# Copyright 2009-2012 Stijn De Weirdt
# Copyright 2010 Dries Verdegem
# Copyright 2010-2012 Kenneth Hoste
# Copyright 2011 Pieter De Baets
# Copyright 2011-2012 Jens Timmerman
#
# This file is part of EasyBuild,
# originally created by the HPC team of the University of Ghent (http://ugent.be/hpc).
#
# http://github.com/hpcugent/easybuild
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
##
"""
EasyBuild support for building and installing Blat, implemented as an easyblock
"""
import os
import platform

import easybuild.tools.environment as env
from easybuild.framework.application import Application
from easybuild.tools.filetools import run_cmd
from easybuild.tools.modules import get_software_root
from easybuild.tools.toolkit import INTEL

class EB_Blat(Application):
    """
    Support for building/installing Blat
    - configure: set BLATHOME 
    - make install: will build in BLATHOME
    """

    def configure(self):
        """Configure Blat by setting BLATHOME"""
        env.set('BLATHOME', self.installdir)
        self.machtype = platform.machine()

    def make(self):
        """Empty make, make install will do make in installdir"""
        pass

    def make_install(self):
        """run make after creating some directories"""
        try:
            os.makedirs(os.path.join(self.installdir, "bin", self.machtype))
            os.makedirs(os.path.join(self.builddir, "lib", self.machtype))
        except OSError, err:
            self.log.error("Creating directories failed: %s" % err)

        # tweak make options
        # LDFLAGS ignored in makefile...
        cflags = " $LDFLAGS"
        makeopts = self.cfg['makeopts']
        if self.toolkit().comp_family() == INTEL:
            # disable specific warning that gcc doesn't complain about
            # required because Blat is built with -Werror
            cflags = " -wr188%s" % cflags
        makeopts += ' CC="$CC%s" MACHTYPE=%s' % (cflags, self.machtype)
        self.cfg['makeopts'] = makeopts

        super(self.__class__, self).make()

    def make_module_req_guess(self):
        """PATH should point to bin/machinetype"""
        guess = super(self.__class__, self).make_module_req_guess()
        guess['PATH'] = guess['PATH'] + ['bin/%s' % self.machtype]
        return guess

    def sanitycheck(self):
        """Custom sanity check paths"""
        self.cfg['sanityCheckPaths'] = {'files':[],
                                'dirs':["bin/%s" % self.machtype]
                              }

        super(self.__class__, self).sanitycheck()
