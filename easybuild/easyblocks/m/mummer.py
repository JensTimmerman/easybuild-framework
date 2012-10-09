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
EasyBuild support for building and installing MUMer, implemented as an easyblock
"""

import shutil

from easybuild.framework.application import Application
from easybuild.tools.filetools import run_cmd


class EB_MUMmer(Application):
    """Support for building and installing MUMmer."""

    def configure(self):
        """Configure MUMmer build by running make check."""
        cmd = "%s make check %s" % (self.getcfg('preconfigopts'), self.getcfg('configopts'))
        run_cmd(cmd, log_all=True, simple=True, log_output=True)
        # build in installation directory
        self.build_in_installdir = True

    def make(self):
        """Build MUMer"""
        makeopts = self.getcfg('makeopts')
        # set all as default make argument
        makeopts = " ".join([makeopts, 'all'])
        super(self.__class__, self).make()

    def make_install(self):
        """Building was performed in build dir, so copy everything over."""
        # remove actuall installdir, shutil doesn't like it to be there
        shutil.rmtree(self.installdir)
        shutil.copytree(self.getcfg('startfrom'), self.installdir, symlinks=True)
        # TODO: we could now actually remove everything that is not in sanityCheckPaths

    def make_module_extra(self):
        """Add the root to path, since this is where the binaries are located"""
        txt = super(self.__class__, self).make_module_extra()
        txt += self.moduleGenerator.prependPaths("PATH", [""])
        return txt

    def sanitycheck(self):
        """Custom sanity check for OpenFOAM"""

        if not self.getcfg('sanityCheckPaths'):

            self.setcfg('sanityCheckPaths', {'files': ['mapview', 'combineMUMs', 'mgaps', 'run-mummer3', 'show-coords',
                                                       'show-snps', 'show-aligns', 'dnadiff', 'mummerplot',
                                                       'nucmer2xfig', 'annotate', 'promer', 'show-diff', 'nucmer',
                                                       'docs', 'delta-filter', 'src', 'run-mummer1', 'gaps', 'mummer',
                                                       'repeat-match', 'scripts', 'show-tiling', 'exact-tandems',
                                                       'aux_bin'
                                                       ],
                                             'dirs': []
                                           })

            self.log.info("Customized sanity check paths: %s" % self.getcfg('sanityCheckPaths'))

        Application.sanitycheck(self)
