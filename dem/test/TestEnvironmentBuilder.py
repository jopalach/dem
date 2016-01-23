import os
import unittest, mock
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest
import dem.EnvironmentBuilder as builder


class TestEnvironmentBuilder(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

        self.base = os.getcwd()
        self.virtualenv_patcher = mock.patch('virtualenv.create_environment')
        self.addCleanup(self.virtualenv_patcher.stop)
        self.mock_virtualenv_create_environment = self.virtualenv_patcher.start()

    def test_willCreateBaseEnvDirectory(self):
        builder.create_dem_env()

        self.assertTrue(os.path.exists('demenv'))

    def test_willCreatePythonDirectory(self):
        builder.create_dem_env()

        self.assertTrue(os.path.exists(os.path.join('demenv', 'python')))

    def test_willCreateDependenciesDirectory(self):
        builder.create_dem_env()

        self.assertTrue(os.path.exists(os.path.join('demenv', 'libs')))

    def test_willCreateVirutalenvInPythonDir(self):
        builder.create_dem_env()

        self.mock_virtualenv_create_environment.assert_called_once_with(os.path.join(self.base, 'demenv', 'python'))


if __name__ == '__main__':
    unittest.main()
