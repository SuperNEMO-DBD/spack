# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import sys

class Gl2ps(CMakePackage):
    """GL2PS is a C library providing high quality vector output for any
    OpenGL application."""

    homepage = "http://www.geuz.org/gl2ps/"
    url      = "http://geuz.org/gl2ps/src/gl2ps-1.3.9.tgz"

    version('1.3.9', sha256='8a680bff120df8bcd78afac276cdc38041fed617f2721bade01213362bcc3640')

    variant('png',  default=True, description='Enable PNG support')
    variant('zlib', default=True, description='Enable compression using ZLIB')
    variant('doc', default=False,
            description='Generate documentation using pdflatex')

    depends_on('cmake@2.4:', type='build')

    depends_on('libpng', when='+png')
    depends_on('zlib',   when='+zlib')
    depends_on('texlive', type='build', when='+doc')

    depends_on('gl')
    depends_on('glu')
    
    # X11 libraries are needed on Linux because CMake's find_package
    # will require them until CMake 3.2:
    if sys.platform == 'linux':
         # GLUT only for the test program?
         depends_on('freeglut')
         # Link on standard CentOS platform is
         # -lGLU -lGL -lSM -lICE -lX11 -lXext -lglut -lXmu -lXi -lz -lpng -lz -lm -lpng -lm 
         depends_on('libsm')
         depends_on('libice')
         depends_on('libx11')
         depends_on('libxext')
         depends_on('libxmu')
         depends_on('libxi')

    def variant_to_bool(self, variant):
        return 'ON' if variant in self.spec else 'OFF'

    def cmake_args(self):
        options = [
            '-DENABLE_PNG={0}'.format(self.variant_to_bool('+png')),
            '-DENABLE_ZLIB={0}'.format(self.variant_to_bool('+zlib')),
        ]
        if '~doc' in self.spec:
            # Make sure we don't look.
            options.append('-DCMAKE_DISABLE_FIND_PACKAGE_LATEX:BOOL=ON')

        return options
