import os
import unittest
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest
from mock import patch, MagicMock

import dem.DevEnvReader as reader

SAMPLE_CONTENT = '''
config:
    remote_locations:
        ['/opt',
        'http://github.com']
packages:
    qt:
        version: 4.8.6
        type: rpm
    json:
        version: 1.8
        type: archive
    Which:
        type: perl
        destination: 'bin'
    git-python:
        type: python
        destination: 'python-site-packages'
    x11:
        version: latest
        type: rpm
        system: yes
'''

SAMPLE_CONTENT_WITH_ONLY_ONE_REMOTE_LOCATION = '''
config:
    remote_locations:
        '/opt'
packages:
    qt:
        version: 4.8.6
        type: rpm
    json:
        version: 1.8
        type: archive
    Which:
        type: perl
    git-python:
        type: python
    x11:
        version: latest
        type: rpm
        system: yes
'''

SAMPLE_CONTENT_WITH_LINUX_AND_ALL_PACKAGES = '''
config:
    remote_locations:
        '/opt'
packages:
    qt:
        version: 4.8.6
        type: rpm
packages-linux:
    json:
        version: 1.8
        type: archive
    Which:
        type: perl
'''

SAMPLE_CONTENT_WITH_WINDOWS_AND_ALL_PACKAGES = '''
config:
    remote_locations:
        '/opt'
packages:
    qt:
        version: 4.8.6
        type: rpm
packages-win32:
    json:
        version: 1.8
        type: archive
    Which:
        type: perl
'''


class TestDevEnvReader(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    @patch('sys.platform', "win32")
    def test_willReadPackagesFromFile(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertNotEquals(packages['qt'], None)
        self.assertNotEquals(packages['json'], None)
        self.assertNotEquals(packages['Which'], None)
        self.assertNotEquals(packages['git-python'], None)
        self.assertNotEquals(packages['x11'], None)

    @patch('sys.platform', "win32")
    def test_willReadVersionFromFile(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertEquals(packages['qt']['version'], '4.8.6')
        self.assertEquals(packages['json']['version'], '1.8')
        self.assertEquals(packages['Which']['version'], 'latest')
        self.assertEquals(packages['git-python']['version'], 'latest')
        self.assertEquals(packages['x11']['version'], 'latest')

    @patch('sys.platform', "win32")
    def test_willReadTypeFromFile(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertEquals(packages['qt']['type'], 'rpm')
        self.assertEquals(packages['json']['type'], 'archive')
        self.assertEquals(packages['Which']['type'], 'perl')
        self.assertEquals(packages['git-python']['type'], 'python')
        self.assertEquals(packages['x11']['type'], 'rpm')

    @patch('sys.platform', "win32")
    def test_willReadTypeFromFile(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertEquals(packages['qt']['destination'], 'dependency-lib')
        self.assertEquals(packages['json']['destination'], 'dependency-lib')
        self.assertEquals(packages['Which']['destination'], 'bin')
        self.assertEquals(packages['git-python']['destination'], 'python-site-packages')
        self.assertEquals(packages['x11']['destination'], 'dependency-lib')

    @patch('sys.platform', "linux")
    @patch('platform.linux_distribution', MagicMock(return_value=('centos', '7.34.21', 'core')))
    @patch('platform.machine', MagicMock(return_value=('i386')))
    def test_willInterpretSingleRemoteLocationAsListWithOSSearchesAdded(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT_WITH_ONLY_ONE_REMOTE_LOCATION)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertEquals(config['remote_locations'], [os.path.join('/opt', 'centos7', 'i386'), os.path.join('/opt', 'rhel7', 'i386'), os.path.join('/opt', 'centos7'), os.path.join('/opt', 'rhel7'), '/opt'])

    @patch('sys.platform', "linux")
    @patch('platform.linux_distribution', MagicMock(return_value=('centos', '7.34.21', 'core')))
    @patch('platform.machine', MagicMock(return_value=('i386')))
    def test_willReadLinuxPackagesFromFile(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT_WITH_LINUX_AND_ALL_PACKAGES)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertNotEquals(packages['qt'], None)
        self.assertNotEquals(packages['json'], None)
        self.assertNotEquals(packages['Which'], None)

    @patch('sys.platform', "win32")
    def test_willReadWindowsPackagesFromFile(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT_WITH_WINDOWS_AND_ALL_PACKAGES)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertNotEquals(packages['qt'], None)
        self.assertNotEquals(packages['json'], None)
        self.assertNotEquals(packages['Which'], None)

    @patch('sys.platform', "win32")
    @patch('platform.machine', MagicMock(return_value=('amd64')))
    def test_wilAddSearchPathsBasedOnWindowsAndArch(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertEquals(config['remote_locations'],
                          [os.path.join('/opt', 'win32', 'x86_64'), os.path.join('/opt', 'win32'), '/opt',
                           os.path.join('http://github.com', 'win32', 'x86_64'),
                           os.path.join('http://github.com', 'win32'), 'http://github.com'])

    def test_will_exit_if_yaml_file_does_not_exist(self):
        with self.assertRaises(SystemExit):
            reader.devenv_from_file('unknown.yaml')


if __name__ == '__main__':
    unittest.main()
