import os
import unittest
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest
from dem import dem as go


class MyTestCase(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()


    def test_willCreateDependenciesFolder(self):
        self.fs.CreateFile('devenv.yaml')

        go.get_dem_packages()

        self.assertTrue(os.path.exists('devenv'))

    def test_willCreateLibrariesFolderWhenGettingAnArchive(self):
        self.fs.CreateFile('devenv.yaml', contents='''
            packages:
                -json:
                    version: 1.8
                    type: archive''')

        go.get_dem_packages()

        self.assertTrue(os.path.exists(os.path.join('devenv', 'libs')))

if __name__ == '__main__':
    unittest.main()
