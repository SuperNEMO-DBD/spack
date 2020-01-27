# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Camp(CMakePackage):
    """C++ multi-purpose reflection library."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/drbenmorgan/camp"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['drbenmorgan']

    #version('7564e57f7b406d1021290cf2260334d57d8df255', sha256='e7963798ca791aa9e918faf84071e669f87fb5de7c1767c41eefd41236f17b17')
    #url      = "https://github.com/drbenmorgan/camp/commit/7564e57f7b406d1021290cf2260334d57d8df255"
    version('supernemo', git='https://github.com/drbenmorgan/camp.git', commit='7564e57f7b406d1021290cf2260334d57d8df255')

    variant('cxxstd',
            default='11',
            values=('11', '14', '17'),
            multi=False,
            description='Use the specified C++ standard when building.')

    depends_on('boost@1.69: cxxstd=11', when='cxxstd=11')
    depends_on('boost@1.69: cxxstd=14', when='cxxstd=14')
    depends_on('boost@1.69: cxxstd=17', when='cxxstd=17')

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.format(self.spec.variants['cxxstd'].value)]
        return args
