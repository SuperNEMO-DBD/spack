# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Bxdecay0(CMakePackage):
    """ C++ port of the Decay0/GENBB fortran Monte Carlo code for the
        generation of standard decay or double beta decay processes for
        various radioactive nuclides of interest
    """

    homepage = "https://github.com/BxCppDev/bxdecay0"
    url      = "https://github.com/BxCppDev/bxdecay0/archive/1.0.1.tar.gz"

    maintainers = ['drbenmorgan']

    version('1.0.1', sha256='fc5afdce221babc0b49b30cbc123cd8d3feac16ac22bef2c3cda00abe693e550')

    depends_on('gsl@2.4:')

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.format(self.spec.variants['cxxstd'].value)]
        return args
