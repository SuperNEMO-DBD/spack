# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


def sanitize_environments(*args):
    for env in args:
        for var in ('PATH', 'CET_PLUGIN_PATH',
                    'LD_LIBRARY_PATH', 'DYLD_LIBRARY_PATH', 'LIBRARY_PATH',
                    'CMAKE_INSTALL_RPATH', 'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class FhiclCpp(CMakePackage):
    """A C++ implementation of the FHiCL configuration language for the art
    suite.
    """

    homepage = 'http://art.fnal.gov/'
    git_base = 'http://cdcvs.fnal.gov/projects/fhicl-cpp'

    version('MVP1a', branch='feature/Spack-MVP1a',
            git=git_base, preferred=True)
    version('MVP', branch='feature/for_spack', git=git_base)
    version('develop', branch='develop', git=git_base)
    version('4.09.02', tag='v4_09_02', git=git_base)
    version('4.09.03', tag='v4_09_03', git=git_base)
    version('4.10.00', tag='v4_10_00', git=git_base)
    version('4.11.00', tag='v4_11_00', git=git_base)

    #patch('fhicl-cpp.unups.patch')
    def patch(self):
        # Temp get rid of Werror on macOS
        filter_file(
            'WERROR',
            '',
            'CMakeLists.txt')

    _cxxstds = ('14', '17')
    variant('cxxstd',
            default='17',
            values=_cxxstds,
            multi=False,
            description='Use the specified C++ standard when building.')

    # Build-only dependencies.
    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules@1.01.01:', type='build')
    depends_on('py-pybind11', type='build')

    # Build / link dependencies.
    for s in _cxxstds:
      depends_on('boost cxxstd=' + s, when='cxxstd=' + s)
      depends_on('cetlib cxxstd=' + s, when='cxxstd=' + s)
      depends_on('cetlib-except cxxstd=' + s, when='cxxstd=' + s)
      depends_on('hep-concurrency cxxstd=' + s, when='cxxstd=' + s)
    
    depends_on('sqlite')
    depends_on('openssl')
    depends_on('python')

    if 'SPACKDEV_GENERATOR' in os.environ:
        generator = os.environ['SPACKDEV_GENERATOR']
        if generator.endswith('Ninja'):
            depends_on('ninja', type='build')

    def url_for_version(self, version):
        url = 'http://cdcvs.fnal.gov/cgi-bin/git_archive.cgi/cvs/projects/{0}.v{1}.tbz2'
        return url.format(self.name, version.underscored)

    def cmake_args(self):
        args = ['-DCMAKE_CXX_STANDARD={0}'.
                format(self.spec.variants['cxxstd'].value)]
        return args

    def setup_environment(self, spack_env, run_env):
        # Path for tests.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup
        sanitize_environments(spack_env, run_env)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        # Binaries.
        spack_env.prepend_path('PATH', self.prefix.bin)
        run_env.prepend_path('PATH', self.prefix.bin)
        spack_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
        run_env.prepend_path('ROOT_INCLUDE_PATH', self.prefix.include)
