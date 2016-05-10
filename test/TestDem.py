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

    @patch('sys.platform', "win32")
    @mock.patch('subprocess.call', MagicMock())
    def test_willCreateDependenciesFolder(self):
        self.fs.CreateFile('devenv.yaml')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists('.devenv'))

    @patch('sys.platform', "win32")
    @mock.patch('subprocess.call', MagicMock())
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
        self.fs.CreateFile('json/eggs.txt', contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('json/eggs.txt')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'eggs.txt')))

    @patch('sys.platform', "win32")
    @patch('sys.stdout', new_callable=StringIO)
    @mock.patch('subprocess.call', MagicMock())
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

        self.assertTrue('Could not find package: json, version: 1.8\n' in mock_stdout.getvalue())

    @patch('sys.platform', "win32")
    @mock.patch('subprocess.call', MagicMock())
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
        self.fs.CreateFile('json/eggs.txt', contents='''
            I like my eggs runny.''')
        self.fs.CreateFile('json/not_my_eggs.txt', contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location1, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('json/eggs.txt')
        with ZipFile(os.path.join(remote_location2, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('json/not_my_eggs.txt')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'eggs.txt')))
        self.assertFalse(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'not_my_eggs.txt')))

    @unittest.skip("FakeFS does not support tar?\n")
    @mock.patch('subprocess.call', MagicMock())
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
    @mock.patch('subprocess.call', MagicMock())
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
    @mock.patch('subprocess.call', MagicMock())
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
    @mock.patch('subprocess.call', MagicMock())
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
        self.fs.CreateFile('json/eggs.txt', contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('json/eggs.txt')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'eggs.txt')))

    @patch('sys.platform', "win32")
    @mock.patch('subprocess.call', MagicMock())
    def test_willInstallWindowsPackagesForWindowsOS(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
                config:
                    remote_locations: ''' + remote_location + '''
                packages-win32:
                    json:
                        version: msvc2015-1.8
                        type: archive''')
        os.makedirs(remote_location)
        self.fs.CreateFile('json/eggs.txt', contents='''
                I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-msvc2015-1.8.zip'), 'w') as myzip:
            myzip.write('json/eggs.txt')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'dependencies', 'json', 'eggs.txt')))


    @patch('sys.platform', "win32")
    @mock.patch('subprocess.call', MagicMock())
    def test_willUnzipToBinaryDestinationWindowsStrippingParentDirectory(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
            config:
                remote_locations: ''' + remote_location + '''
            packages:
                json:
                    version: 1.8
                    type: archive
                    destination: bin''')
        os.makedirs(remote_location)
        self.fs.CreateFile('eggs.exe', contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('eggs.exe')

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'Scripts', 'eggs.exe')))

    @patch('sys.platform', "linux")
    @patch('platform.linux_distribution', MagicMock(return_value=('centos', '7.34.21', 'core')))
    @mock.patch('subprocess.call', MagicMock())
    def test_willUnzipToBinaryDestinationLinuxStrippingParentDirectory(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
               config:
                   remote_locations: ''' + remote_location + '''
               packages:
                   json:
                       version: 1.8
                       type: archive
                       destination: bin''')
        os.makedirs(remote_location)
        self.fs.CreateFile('eggs.exe', contents='''
               I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write('eggs.exe')

        go.get_dem_packages(self.project)
        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'bin', 'eggs.exe')))


    @patch('sys.platform', "win32")
    @mock.patch('subprocess.call', MagicMock())
    def test_willUnzipToPythonSitePackagesDestinationWindowsStrippingParentDirectory(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
            config:
                remote_locations: ''' + remote_location + '''
            packages:
                json:
                    version: 1.8
                    type: archive
                    destination: python-site-packages''')
        os.makedirs(remote_location)
        self.fs.CreateFile(os.path.join('json', 'eggs.exe'), contents='''
            I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write(os.path.join('json', 'eggs.exe'))

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'Lib', 'site-packages', 'json', 'eggs.exe')))


    @patch('sys.platform', "linux2")
    @patch('platform.linux_distribution', MagicMock(return_value=('centos', '7.34.21', 'core')))
    @mock.patch('subprocess.call', MagicMock())
    def test_willUnzipToPythonSitePackagesDestinationLinuxStrippingParentDirectory(self):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
               config:
                   remote_locations: ''' + remote_location + '''
               packages:
                   json:
                       version: 1.8
                       type: archive
                       destination: python-site-packages''')
        os.makedirs(remote_location)
        self.fs.CreateFile(os.path.join('json', 'eggs.exe'), contents='''
               I like my eggs runny.''')

        with ZipFile(os.path.join(remote_location, 'json-1.8.zip'), 'w') as myzip:
            myzip.write(os.path.join('json', 'eggs.exe'))

        go.get_dem_packages(self.project)

        self.assertTrue(os.path.exists(os.path.join('.devenv', self.project, 'lib', 'python2.7', 'site-packages', 'json', 'eggs.exe')))

    @patch('sys.platform', "win32")
    @patch('wget.download')
    @mock.patch('subprocess.call', MagicMock())
    def test_willDownloadUrlToPythonSitePackagesDestinationWindowsStrippingParentDirectory(self, mock_wget):
        self.fs.CreateFile('devenv.yaml', contents='''
                packages:
                    qtcwatchdog:
                        version: 1.0.1
                        type: url
                        url: https://github.com/ismacaulay/qtcwatchdog/archive/v1.0.1.zip
                        destination: python-site-packages''')

        def wget_side_effect(url, out):
            remote_location = os.path.join('.devenv', self.project, 'downloads')
            self.fs.CreateFile(os.path.join('qtcwatchdog', 'qtc.py'), contents='''
                       I like my eggs runny.''')

            with ZipFile(os.path.join(remote_location, 'qtcwatchdog-1.0.1.zip'), 'w') as myzip:
                myzip.write(os.path.join('qtcwatchdog', 'qtc.py'))

        mock_wget.side_effect = wget_side_effect
        go.get_dem_packages(self.project)

        self.assertTrue(
            os.path.exists(os.path.join('.devenv', self.project, 'Lib', 'site-packages', 'qtcwatchdog')))
        self.assertTrue(
            os.path.exists(os.path.join('.devenv', self.project, 'Lib', 'site-packages', 'qtcwatchdog', 'qtc.py')))

    @patch('sys.platform', "win32")
    @patch('sys.stdout', new_callable=StringIO)
    @mock.patch('subprocess.call', MagicMock())
    def test_will_not_extract_already_installed_archive(self, mock_stdout):
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
        with open('devenv.yaml', 'a+') as f:
            f.write('\n\n')

        go.get_dem_packages(self.project)

        self.assertTrue('json-1.8 already installed' in mock_stdout.getvalue())

    @patch('sys.platform', "win32")
    @patch('git.Repo.clone_from')
    @mock.patch('subprocess.call', MagicMock())
    def test_willCloneGitRepositoryAndCheckoutShaToARelativeDirectory(self, mock_clone):
        self.fs.CreateFile('devenv.yaml', contents='''
                   config:
                   packages:
                       qtcwatchdog:
                           version: 72f3588eef1019bac8788fa58c52722dfa7c4d28
                           type: git
                           url: https://github.com/ismacaulay/qtcwatchdog
                           destination: code/python/''')

        mock_repo = MagicMock()
        def clone_side_effect(url, destination):
            os.makedirs(destination)
            self.fs.CreateFile(os.path.join(destination, 'qtc.py'), contents='''
                          I like my eggs runny.''')
            return mock_repo

        mock_clone.side_effect = clone_side_effect
        go.get_dem_packages(self.project)
        self.assertTrue(
            os.path.exists(os.path.join('code/python/', 'qtcwatchdog')))

    @patch('sys.platform', "win32")
    @patch('subprocess.call')
    @patch('sys.stdout', new_callable=StringIO)
    def test_will_not_extract_already_installed_archive(self, mock_stdout, mock_subprocess):
        remote_location = os.path.abspath(os.path.join(os.pathsep, 'opt'))
        self.fs.CreateFile('devenv.yaml', contents='''
            config:
                remote_locations: ''' + remote_location + '''
            packages:
                json:
                    version: 1.8
                    type: rpm''')
        os.makedirs(remote_location)

        go.get_dem_packages(self.project)
        with open('devenv.yaml', 'a+') as f:
            f.write('\n\n')

        go.get_dem_packages(self.project)

        self.assertTrue('json-1.8 already installed' in mock_stdout.getvalue())




if __name__ == '__main__':
    unittest.main()
