import io
import os
import unittest, mock
from tarfile import TarFile
from zipfile import ZipFile

try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest

from dem import dem as go


class MyDem(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.project = 'project'

        # Fix for python 3+
        io.open = open

        # mock out virtual env since it still has a case sensitive bug in windows
        self.mock_virtual_env_patcher = mock.patch('virtualenv.create_environment')
        self.addCleanup(self.mock_virtual_env_patcher.stop)
        self.mock_virtual_env = self.mock_virtual_env_patcher.start()
        self.mock_virtual_env.side_effect = self.create_environment

    def create_environment(self, path):
        pass

    def test_willCreateDependenciesFolder(self):
        self.fs.CreateFile('devenv.yaml')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists('.devenv'))

    def test_willUnzipDependencyIntoDependenciesDirectory(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
            config:
                remote_locations: ''' + remote_location + '''
            packages:
                json:
                    version: 1.8
                    type: archive''')
        os.makedirs(remote_location)
        self.fs.CreateFile('eggs.txt', contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('eggs.txt')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'eggs.txt')))

    @patch('sys.stdout', new_callable=StringIO)
    def test_willPrintMessageWhenArchivedPackageCannotBeFound(self, mock_stdout):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
            config:
                remote_locations: ''' + remote_location + '''
            packages:
                json:
                    version: 1.8
                    type: archive''')
        os.makedirs('not_opts')
        self.fs.CreateFile('eggs.txt', contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join('not_opts', 'json-1.8.zip'), 'w') as myzip:
            myzip.write('eggs.txt')

        go.get_dem_packages(self.project)

        self.assertEquals(mock_stdout.getvalue(), 'Could not find package: json, version: 1.8\n')

    def test_willInstallFirstPackageFound(self):
        remote_location1 = os.path.abspath(os.path.join(os.pathsep, 'opt1'))
        remote_location2 = os.path.abspath(os.path.join(os.pathsep, 'opt2'))
        self.fs.CreateFile('devenv.yaml', contents='''
            config:
                remote_locations: [\'''' + remote_location1 + '\', \'' + remote_location2 + '''\']
            packages:
                json:
                    version: 1.8
                    type: archive''')

        os.makedirs(remote_location1)
        os.makedirs(remote_location2)
        self.fs.CreateFile('eggs.txt', contents='''
            I like my eggs runny.''')
        self.fs.CreateFile('not_my_eggs.txt', contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location1, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('eggs.txt')
        with ZipFile(os.path.join(remote_location2, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('not_my_eggs.txt')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'eggs.txt')))
        self.assertFalse(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'not_my_eggs.txt')))

    @unittest.skip("FakeFS does not support tar?")
    def test_willUntarDependencyIntoLibsDirectory(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
            config:
                remote_locations: ''' + remote_location + '''
            packages:
                json:
                    version: 1.8
                    type: archive''')
        os.makedirs(remote_location)
        self.fs.CreateFile('eggs.txt', contents='''
            I like my eggs runny.''')

        with TarFile.open(os.path.join(remote_location, 'json-1.8.tar.gz'), 'w:gz') as tar:
            tar.add('eggs.txt')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'eggs.txt')))

    @patch('sys.platform', "win32")
    def test_willNotInstallLinuxPackagesForWindowsOS(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
            config:
                remote_locations: ''' + remote_location + '''
            packages-linux:
                json:
                    version: 1.8
                    type: archive''')
        os.makedirs(remote_location)
        self.fs.CreateFile('eggs.txt', contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('eggs.txt')

        go.get_dem_packages(self.project)

        self.assertFalse(os.path.exists(os.path.join('.devenv', 'libs', 'json', 'eggs.txt')))

    @patch('sys.platform', "linux")
    @patch('platform.linux_distribution', MagicMock(return_value=('centos', '7.34.21', 'core')))
    def test_willNotInstallWindowsPackagesForLinuxOS(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
                config:
                    remote_locations: ''' + remote_location + '''
                packages-win32:
                    json:
                        version: 1.8
                        type: archive''')
        os.makedirs(remote_location)
        self.fs.CreateFile('eggs.txt', contents='''
                I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('eggs.txt')

        go.get_dem_packages(self.project)

        self.assertFalse(os.path.exists(os.path.join('.devenv', 'libs', 'json', 'eggs.txt')))

    @patch('sys.platform', "linux")
    @patch('platform.linux_distribution', MagicMock(return_value=('centos', '7.34.21', 'core')))
    def test_willInstallLinuxPackagesForLinuxOS(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
            config:
                remote_locations: ''' + remote_location + '''
            packages-linux:
                json:
                    version: 1.8
                    type: archive''')
        os.makedirs(remote_location)
        self.fs.CreateFile('eggs.txt', contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('eggs.txt')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'eggs.txt')))

    @patch('sys.platform', "win32")
    def test_willInstallWindowsPackagesForWindowsOS(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
                config:
                    remote_locations: ''' + remote_location + '''
                packages-win32:
                    json:
                        version: 1.8
                        type: archive''')
        os.makedirs(remote_location)
        self.fs.CreateFile('eggs.txt', contents='''
                I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('eggs.txt')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'eggs.txt')))


if __name__ == '__main__':
    unittest.main()
