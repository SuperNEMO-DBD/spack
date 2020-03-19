# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.operating_systems.mac_os import macos_version
import sys

class Qt5Base(Package):
    """Qt5 Core Libraries (SuperNEMO Packaging)
    """

    homepage = "http://qt-project.org/"
    url = "http://download.qt.io/official_releases/qt/5.12/5.12.6/submodules/qtbase-everywhere-src-5.12.6.tar.xz"
    version('5.12.6', sha256='6ab52649d74d7c1728cf4a6cf335d1142b3bf617d476e2857eb7961ef43f9f27')

    # Add required QtSVG module as a resource for now
    # Not clear if Qt modules can be built/installed separately at the moment
    resource(
        name='qt5svg',
        url="http://download.qt.io/official_releases/qt/5.12/5.12.6/submodules/qtsvg-everywhere-src-5.12.6.tar.xz",
        sha256="46243e6c425827ab4e91fbe31567f683ff14cb01d12f9f7543a83a571228ef8f",
        destination='qt5svg',
        placement='qt5svg'
        )

    # Qt5 requires a full Xcode, so make sure we have it
    use_xcode = True

    # In homebrew, we have deps:
    depends_on('pkgconfig', type='build')
    depends_on('freetype')
    depends_on('libjpeg')
    depends_on('libpng')
    depends_on("openssl@1.0:")
    # PCRE2 doesn't seem to work yet...
    #depends_on('pcre')
    # Sqlite must have column_metadata variant
    depends_on('sqlite+column_metadata')
    depends_on('zlib')

    # -qt-xcb, fontconfig on linux
    #

    def setup_build_environment(self, env):
        env.set('MAKEFLAGS', '-j{0}'.format(make_jobs))

    def setup_run_environment(self, env):
        env.set('QTDIR', self.prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('QTDIR', self.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        module.qmake = Executable(join_path(self.spec.prefix.bin, 'qmake'))

    # Configure first?
    def configure(self):
        config_args = [
            '-prefix', self.prefix,
            '-v',
            '-opensource',
            '-confirm-license',
            '-release',
            '-strip',
            '-shared',
            '-no-static',
            '-no-pch',
            '-optimized-qmake',
            # These can be updated when we can fully suppprt microarchitecture opts
            '-no-avx',
            '-no-avx2',
            '-nomake', 'examples',
            '-nomake', 'tests',
            '-pkg-config',
            '-no-sql-mysql',
            '-no-sql-psql',
        ]

        # Despite pkg-config, Qt needs some help to use Spack's
        # packages:
        openssl = self.spec['openssl']
        config_args.extend([
            '-openssl-linked',
            '{0}'.format(openssl.libs.search_flags),
            '{0}'.format(openssl.headers.include_flags)
            ])

        freetype = self.spec['freetype']
        config_args.extend([
            '-system-freetype',
            '-I{0}/freetype2'.format(self.spec['freetype'].prefix.include)
            ])

        png = self.spec['libpng']
        jpeg = self.spec['jpeg']
        zlib = self.spec['zlib']
        config_args.extend([
            '-system-libpng',
            '{0}'.format(png.libs.search_flags),
            '{0}'.format(png.headers.include_flags),
            '-system-libjpeg',
            '{0}'.format(jpeg.libs.search_flags),
            '{0}'.format(jpeg.headers.include_flags),
            '-system-zlib',
            '{0}'.format(zlib.libs.search_flags),
            '{0}'.format(zlib.headers.include_flags)
            ])

        sqlite = self.spec['sqlite']
        config_args.extend([
            '-system-sqlite',
            '{0}'.format(sqlite.libs.search_flags),
            '{0}'.format(sqlite.headers.include_flags)
             ])

        # Portable binaries for kernels < 3.17 cannot be created without
        # these flags. In particular, they are required to allow modern
        # containers to run on older systems.
        if sys.platform == 'linux':
            config_args.extend(["-no-feature-renameat2", "-no-feature-getentropy"])

        # Always build for host platform
        if sys.platform == 'darwin':
            config_args.extend(['QMAKE_MACOSX_DEPLOYMENT_TARGET={0}'.format(macos_version().up_to(2))])

        configure(*config_args)

    def install(self, spec, prefix):
        self.configure()
        make()
        make("install")

    @run_after('install')
    def install_qt5svg(self):
        qmake = Executable(join_path(self.spec.prefix.bin, 'qmake'))
        with working_dir('qt5svg/qt5svg'):
            qmake()
            make("install")

