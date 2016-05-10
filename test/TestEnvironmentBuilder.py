import os
import unittest, mock
import pyfakefs.fake_filesystem_unittest as fake_filesystem_unittest
from dem.EnvironmentBuilder import EnvironmentBuilder
from dem.DevEnvReader import Config

class TestEnvironmentBuilder(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self._config = mock.MagicMock(spec=Config)
        self._config.has_http_proxy.return_value = False

    @mock.patch('virtualenv.create_environment')
    @mock.patch('subprocess.call')
    def test_will_create_devenv_dir(self, mock_virtualenv, mock_subpprocess):
        EnvironmentBuilder.build('', self._config)

        self.assertTrue(os.path.exists('.devenv'))

    @mock.patch('virtualenv.create_environment')
    @mock.patch('subprocess.call')
    def test_will_create_project_dir(self, mock_virtualenv, mock_subpprocess):
        EnvironmentBuilder.build('project', self._config)

        self.assertTrue(os.path.exists(os.path.join('.devenv', 'project')))

    @mock.patch('virtualenv.create_environment')
    @mock.patch('subprocess.call')
    def test_will_create_dependencies_dir(self, mock_virtualenv, mock_subpprocess):
        EnvironmentBuilder.build('project', self._config)

        self.assertTrue(os.path.exists(os.path.join('.devenv', 'project', 'dependencies')))

    @mock.patch('subprocess.call')
    @mock.patch('virtualenv.create_environment')
    def test_will_create_virtualenv_in_devenv_dir(self, mock_virtualenv, mock_subpprocess):
        EnvironmentBuilder.build('project', self._config)

        mock_virtualenv.assert_called_once_with(os.path.join(os.getcwd(), '.devenv', 'project'))

    @mock.patch('subprocess.call')
    @mock.patch('virtualenv.create_environment')
    def test_will_create_downloads_dir(self, mock_virtualenv, mock_subpprocess):
        EnvironmentBuilder.build('project', self._config)

        self.assertTrue(os.path.exists(os.path.join('.devenv', 'project', 'downloads')))

if __name__ == '__main__':
    unittest.main()
