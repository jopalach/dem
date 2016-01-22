import os
import unittest
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest
from dem import dem as go


class MyTestCase(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self.fs.CreateFile('dependencies.yaml')

    def test_willCreateDependenciesFolder(self):
        go.get_dem_packages()
        self.assertTrue(os.path.exists('dependencies'))


if __name__ == '__main__':
    unittest.main()
