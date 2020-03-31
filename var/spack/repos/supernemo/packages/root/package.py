# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install root
#
# You can edit this file again by typing:
#
#     spack edit root
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Root(CMakePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://root.cern.ch"
    url      = "https://root.cern/download/root_v6.18.04.source.tar.gz"

    maintainers = ['drbenmorgan']

    version('6.18.04', sha256='315a85fc8363f8eb1bffa0decbf126121258f79bd273513ed64795675485cfa4')

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    #variant('davix', default=True,
    #        description='Compile with external Davix')
    #variant('python', default=True,
    #        description='Enable Python ROOT bindings')

    # Always required
    # - Direct (without these Root will build/download them without
    # any way to disable
    depends_on('cmake@3.9:', type='build', when='@6.18.00:')
    depends_on('pkgconfig', type='build')
    depends_on('freetype')
    depends_on('lz4')
    depends_on('pcre')
    depends_on('xxhash')
    depends_on('xz')
    depends_on('zlib')

    #depends_on('jpeg')
    #depends_on('libpng')
    #depends_on('lzma')
    #depends_on('ncurses')
    #depends_on('openssl')

# needed by mathmore and tmva
    #depends_on('gsl')


    #depends_on('davix @0.7.1:', when='+davix')
    #depends_on('python@3:', when='+python', type=('build', 'run'))

    # Default needed with imt=ON, tbb=ON
    #depends_on('tbb')

    # Default needed with vdt=ON
    #depends_on('vdt')

    def cmake_args(self):
        args = ["-Dminimal=ON",
                "-Dfail-on-missing=ON"]
        args.append("-Dcxx{0}=ON".format(self.spec.variants['cxxstd'].value))
         #"-Ddavix=OFF", # optional on +davix
                #"-Dfftw3=OFF",
                #"-Dgfal=OFF",
                #"-Dmysql=OFF",
                #"-Doracle=OFF",
                #"-Dpgsql=OFF",
                #"-Dpythia6=OFF",
                #"-Dpythia8=OFF",
                #"-Dtmva-pymva=OFF",
                #"-Dxrootd=OFF"]
        return args
