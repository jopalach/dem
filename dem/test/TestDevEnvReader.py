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
    git-python:
        type: python
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

    def test_willReadPackagesFromFile(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertNotEquals(packages['qt'], None)
        self.assertNotEquals(packages['json'], None)
        self.assertNotEquals(packages['Which'], None)
        self.assertNotEquals(packages['git-python'], None)
        self.assertNotEquals(packages['x11'], None)

    def test_willReadVersionFromFile(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertEquals(packages['qt']['version'], '4.8.6')
        self.assertEquals(packages['json']['version'], '1.8')
        self.assertEquals(packages['Which']['version'], 'latest')
        self.assertEquals(packages['git-python']['version'], 'latest')
        self.assertEquals(packages['x11']['version'], 'latest')

    def test_willReadTypeFromFile(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertEquals(packages['qt']['type'], 'rpm')
        self.assertEquals(packages['json']['type'], 'archive')
        self.assertEquals(packages['Which']['type'], 'perl')
        self.assertEquals(packages['git-python']['type'], 'python')
        self.assertEquals(packages['x11']['type'], 'rpm')

    def test_willReadListOfRepositoryLocations(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertEquals(config['remote_locations'], ['/opt', 'http://github.com'])

    def test_willInterpretSingleRemoteLocationAsList(self):
        self.fs.CreateFile('devenv.yaml', contents=SAMPLE_CONTENT_WITH_ONLY_ONE_REMOTE_LOCATION)

        (config, packages) = reader.devenv_from_file('devenv.yaml')

        self.assertEquals(config['remote_locations'], ['/opt'])

    @patch('sys.platform', "linux")
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

    def test_will_exit_if_yaml_file_does_not_exist(self):
        with self.assertRaises(SystemExit):
            reader.devenv_from_file('unknown.yaml')


if __name__ == '__main__':
    unittest.main()
