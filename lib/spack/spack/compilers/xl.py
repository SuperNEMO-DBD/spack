# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.compiler import Compiler, UnsupportedCompilerFlag
from spack.version import ver


class Xl(Compiler):
    # Subclasses use possible names of C compiler
    cc_names = ['xlc']

    # Subclasses use possible names of C++ compiler
    cxx_names = ['xlC', 'xlc++']

    # Subclasses use possible names of Fortran 77 compiler
    f77_names = ['xlf']

    # Subclasses use possible names of Fortran 90 compiler
    fc_names = ['xlf90', 'xlf95', 'xlf2003', 'xlf2008']

    # Named wrapper links within build_env_path
    link_paths = {'cc': 'xl/xlc',
                  'cxx': 'xl/xlc++',
                  'f77': 'xl/xlf',
                  'fc': 'xl/xlf90'}

    version_argument = '-qversion'
    version_regex = r'([0-9]?[0-9]\.[0-9])'

    @property
    def openmp_flag(self):
        return "-qsmp=omp"

    @property
    def cxx11_flag(self):
        if self.version < ver('13.1'):
            raise UnsupportedCompilerFlag(self,
                                          "the C++11 standard",
                                          "cxx11_flag",
                                          "< 13.1")
        else:
            return "-qlanglvl=extended0x"

    @property
    def c99_flag(self):
        return '-std=c99'

    @property
    def c11_flag(self):
        return '-std=c11'

    @property
    def pic_flag(self):
        return "-qpic"

    @property
    def fflags(self):
        # The -qzerosize flag is effective only for the Fortran 77
        # compilers and allows the use of zero size objects.
        # For Fortran 90 and beyond, it is set by default and has not impact.
        # Its use has no negative side effects.
        return "-qzerosize"

    @classmethod
    def fc_version(cls, fc):
        # The fortran and C/C++ versions of the XL compiler are always
        # two units apart.  By this we mean that the fortran release that
        # goes with XL C/C++ 11.1 is 13.1.  Having such a difference in
        # version number is confusing spack quite a lot.  Most notably
        # if you keep the versions as is the default xl compiler will
        # only have fortran and no C/C++.  So we associate the Fortran
        # compiler with the version associated to the C/C++ compiler.
        # One last stumble. Version numbers over 10 have at least a .1
        # those under 10 a .0. There is no xlf 9.x or under currently
        # available. BG/P and BG/L can such a compiler mix and possibly
        # older version of AIX and linux on power.
        fortran_version = cls.default_version(fc)
        if fortran_version >= 16:
            # Starting with version 16.1, the XL C and Fortran compilers
            # have the same version.  So no need to downgrade the Fortran
            # compiler version to match that of the C compiler version.
            return str(fortran_version)
        c_version = float(fortran_version) - 2
        if c_version < 10:
            c_version = c_version - 0.1
        return str(c_version)

    @classmethod
    def f77_version(cls, f77):
        return cls.fc_version(f77)
