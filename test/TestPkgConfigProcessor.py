import unittest, mock
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest
import os

from dem.pkgconfig import PkgConfigProcessor
from dem.cache import PackageCache
from dem import DevEnvReader as reader

SAMPLE_YAML_CONTENT = '''
config:
    remote_locations:
        ['/opt',
        'http://github.com']
packages:
    qt:
        version: 4.8.6
        type: archive
        pkg-config: lib/pkgconfig
    json:
        version: 1.9
        type: archive
'''

SAMPLE_CACHE_CONTENT = '''
{
    "md5": "b084deb42d4daefe7c29d4eae24c2d2d",

    "packages":
    {
        "qt": {"version": "4.8.6", "type": "local", "install_locations": [".devenv/dependencies/qt"]},
        "json": {"version": "1.8", "type": "local", "install_locations": [".devenv/dependencies/json"]},
        "gcc": {"version": "5.2.0", "type": "system"}
    }
}
'''

SAMPLE_PKG_CONFIG_FILE = '''
prefix=/usr/local
exec_prefix=${prefix}
includedir=${prefix}/include
libdir=${exec_prefix}/lib

Name: foo
Description: The foo library
Version: 1.0.0
Cflags: -I${includedir}/foo
Libs: -L${libdir} -lfoo -L${prefix}/lib
'''

SAMPLE_PKG_CONFIG_FILE_WITH_NO_PREFIX = '''
exec_prefix=${prefix}
includedir=${prefix}/include
libdir=${exec_prefix}/lib

Name: foo
Description: The foo library
Version: 1.0.0
Cflags: -I${includedir}/foo
Libs: -L${libdir} -lfoo -L${prefix}/lib
'''

EXPECTED_SAMPLE_PKG_CONFIG_FILE = '''
prefix=/base_path/.devenv/dependencies/qt
exec_prefix=${prefix}
includedir=${prefix}/include
libdir=${exec_prefix}/lib

Name: foo
Description: The foo library
Version: 1.0.0
Cflags: -I${includedir}/foo
Libs: -L${libdir} -lfoo -L${prefix}/lib
'''
class TestPkgConfigProcessor(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self._base_path = os.path.abspath('base_path')
        self._yaml_file = os.path.join(self._base_path, 'devenv.yaml')
        self._dev_env = os.path.join(self._base_path, '.devenv')
        self._deps = os.path.join(self._dev_env, 'dependencies')
        self._cache_file = os.path.join(self._dev_env, 'cache.json')

        self.setup_directories()

    @mock.patch('sys.platform', "win32")
    def test_will_replace_prefix_variable_in_all_pc_files(self):
        self.setup_files(SAMPLE_YAML_CONTENT, SAMPLE_CACHE_CONTENT)
        self.create_dependency_directory(os.path.join('qt', 'lib'))
        self.create_dependency_directory(os.path.join('qt', 'lib', 'pkgconfig'))
        self.create_dependency_file(os.path.join('qt', 'lib', 'pkgconfig', 'Qt5Core.pc'), SAMPLE_PKG_CONFIG_FILE)

        cache = PackageCache('myProject', self._base_path)
        (_, packages) = reader.devenv_from_file(self._yaml_file)

        PkgConfigProcessor.replace_prefix(cache.install_locations('qt'), packages['qt']['pkg-config'])

        with open(os.path.join(self._deps, 'qt', 'lib', 'pkgconfig', 'Qt5Core.pc')) as f:
            replaced_pkg_config_data = f.readlines()

        self.assertEqual(''.join(replaced_pkg_config_data), EXPECTED_SAMPLE_PKG_CONFIG_FILE)

    @mock.patch('sys.platform', "win32")
    def test_will_not_replace_anything_if_prefix_var_missing(self):
        self.setup_files(SAMPLE_YAML_CONTENT, SAMPLE_CACHE_CONTENT)
        self.create_dependency_directory(os.path.join('qt', 'lib'))
        self.create_dependency_directory(os.path.join('qt', 'lib', 'pkgconfig'))
        self.create_dependency_file(os.path.join('qt', 'lib', 'pkgconfig', 'Qt5Core.pc'), SAMPLE_PKG_CONFIG_FILE_WITH_NO_PREFIX)

        cache = PackageCache('myProject', self._base_path)
        (_, packages) = reader.devenv_from_file(self._yaml_file)

        PkgConfigProcessor.replace_prefix(cache.install_locations('qt'), packages['qt']['pkg-config'])

        with open(os.path.join(self._deps, 'qt', 'lib', 'pkgconfig', 'Qt5Core.pc')) as f:
            replaced_pkg_config_data = f.readlines()

        self.assertEqual(''.join(replaced_pkg_config_data), SAMPLE_PKG_CONFIG_FILE_WITH_NO_PREFIX)

    @mock.patch('sys.platform', "win32")
    def test_will_only_open_pc_files(self):
        self.setup_files(SAMPLE_YAML_CONTENT, SAMPLE_CACHE_CONTENT)
        self.create_dependency_directory(os.path.join('qt', 'lib'))
        self.create_dependency_directory(os.path.join('qt', 'lib', 'pkgconfig'))
        self.create_dependency_file(os.path.join('qt', 'lib', 'pkgconfig', 'Qt5Core.pc'),
                                    SAMPLE_PKG_CONFIG_FILE)
        self.create_dependency_file(os.path.join('qt', 'lib', 'pkgconfig', 'text.txt'),
                                    SAMPLE_PKG_CONFIG_FILE)

        open_patcher = mock.patch('dem.pkgconfig.open', mock.mock_open())
        self.addCleanup(open_patcher.stop)
        mock_open = open_patcher.start()

        cache = PackageCache('myProject', self._base_path)
        (_, packages) = reader.devenv_from_file(self._yaml_file)

        PkgConfigProcessor.replace_prefix(cache.install_locations('qt'), packages['qt']['pkg-config'])

        mock_open.assert_any_call(os.path.join(self._deps, 'qt', 'lib', 'pkgconfig', 'Qt5Core.pc'))
        mock_open.assert_any_call(os.path.join(self._deps, 'qt', 'lib', 'pkgconfig', 'Qt5Core.pc'), 'w+')

    def setup_directories(self):
        self.fs.CreateDirectory(self._base_path)
        self.fs.CreateDirectory(self._dev_env)
        self.fs.CreateDirectory(self._deps)

    def setup_files(self, yaml_file_data, cache_file_data):
        self.fs.CreateFile(self._yaml_file, contents=yaml_file_data)
        self.fs.CreateFile(self._cache_file, contents=cache_file_data)

    def create_dependency_directory(self, path):
        self.fs.CreateDirectory(os.path.join(self._deps, path))

    def create_dependency_file(self, path, data):
        self.fs.CreateFile(os.path.join(self._deps, path), contents=data)

if __name__ == '__main__':
    unittest.main()
