import io
import os
import unittest
from unittest.mock import patch
from zipfile import ZipFile

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest

from dem import dem as go


class MyDem(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        # Fix for python 3+
        io.open = open

    def test_willCreateDependenciesFolder(self):
        self.fs.CreateFile('devenv.yaml')

        go.get_dem_packages()

        self.assertTrue(os.path.exists('devenv'))

    def test_willCreateLibrariesFolderWhenGettingAnArchive(self):
        self.fs.CreateFile('devenv.yaml', contents='''
            packages:
                json:
                    version: 1.8
                    type: archive''')

        go.get_dem_packages()

        self.assertTrue(os.path.exists(os.path.join('devenv', 'libs')))

    def test_willUnzipDependencyIntoLibsDirectory(self):
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

        go.get_dem_packages()

        self.assertTrue(os.path.exists(os.path.join('devenv', 'libs', 'json', 'eggs.txt')))

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

        go.get_dem_packages()

        self.assertEquals(mock_stdout.getvalue(), 'Could not find package: json, version: 1.8\n')




if __name__ == '__main__':
    unittest.main()
