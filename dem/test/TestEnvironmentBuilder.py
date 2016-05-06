import os
import unittest, mock
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest
import pyfakefs.fake_filesystem_shutil as fake_shutil

from dem.EnvironmentBuilder import EnvironmentBuilder


class TestEnvironmentBuilder(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    @mock.patch('virtualenv.create_environment')
    def test_will_create_devenv_dir(self, mock_virtualenv):
        EnvironmentBuilder.build('')

        self.assertTrue(os.path.exists('.devenv'))

    @mock.patch('virtualenv.create_environment')
    def test_will_create_project_dir(self, mock_virtualenv):
        EnvironmentBuilder.build('project')

        self.assertTrue(os.path.exists(os.path.join('.devenv', 'project')))

    @mock.patch('virtualenv.create_environment')
    def test_will_create_dependencies_dir(self, mock_virtualenv):
        EnvironmentBuilder.build('project')

        self.assertTrue(os.path.exists(os.path.join('.devenv', 'project', 'dependencies')))

    @mock.patch('virtualenv.create_environment')
    def test_will_create_virtualenv_in_devenv_dir(self, mock_virtualenv):
        EnvironmentBuilder.build('project')

        mock_virtualenv.assert_called_once_with(os.path.join(os.getcwd(), '.devenv', 'project'))


if __name__ == '__main__':
    unittest.main()
