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
                    'CMAKE_PREFIX_PATH', 'ROOT_INCLUDE_PATH'):
            env.prune_duplicate_paths(var)
            env.deprioritize_system_paths(var)


class Canvas(CMakePackage):
    """The underpinnings for the art suite."""

    homepage = 'http://art.fnal.gov/'
    git_base = 'http://cdcvs.fnal.gov/projects/canvas'

    version('MVP1a', branch='feature/Spack-MVP1a',
            git=git_base, preferred=True)
    version('MVP', branch='feature/for_spack', git=git_base)
    version('develop', branch='develop', git=git_base)
    version('3.05.00', tag='v3_05_00', git=git_base)
    version('3.05.01', tag='v3_05_01', git=git_base)
    version('3.07.03', tag='v3_07_03', git=git_base)
    version('3.07.04', tag='v3_07_04', git=git_base)
    version('3.08.00', tag='v3_08_00', git=git_base)
    version('3.05.00', tag='v3_05_00', git=git_base)
    version('3.05.01', tag='v3_05_01', git=git_base)
    version('3.07.03', tag='v3_07_03', git=git_base)
    version('3.07.04', tag='v3_07_04', git=git_base)
    version('3.08.00', tag='v3_08_00', git=git_base)

    _cxxstds = ('14', '17')
    variant('cxxstd',
            default='17',
            values=_cxxstds,
            multi=False,
            description='Use the specified C++ standard when building.')

    # Build-only dependencies.
    depends_on('cmake@3.11:', type='build')
    depends_on('cetmodules@1.01.01:', type='build')

    for s in _cxxstds:
      depends_on('clhep cxxstd=' + s, when='cxxstd=' + s)
      depends_on('boost cxxstd=' + s, when='cxxstd=' + s)
      depends_on('cetlib cxxstd=' + s, when='cxxstd=' + s)
      depends_on('cetlib-except cxxstd=' + s, when='cxxstd=' + s)
      depends_on('cppunit cxxstd=' + s, when='cxxstd=' + s)
      depends_on('fhicl-cpp cxxstd=' + s, when='cxxstd=' + s)
      depends_on('hep-concurrency cxxstd=' + s, when='cxxstd=' + s)
      depends_on('messagefacility cxxstd=' + s, when='cxxstd=' + s)
      depends_on('tbb cxxstd=' + s, when='cxxstd=' + s)
      # Range-v3 is header only, but defines the cxxstd variant
      depends_on('range-v3 cxxstd=' + s, when='cxxstd=' + s)

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
        # Binaries.
        spack_env.prepend_path('PATH', os.path.join(self.build_directory, 'bin'))
        # Cleanup.
        sanitize_environments(spack_env, run_env)
