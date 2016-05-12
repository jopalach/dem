import os
import unittest

from dem.project.cache import PackageCache
from dem.project.reader import Config

try:
    from mock import patch, MagicMock
except ImportError:
    from unittest.mock import patch, MagicMock

from dem.dependency.pip import PipRunner, PipInstaller
from dem.project.utils import Utils


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.directory_name = 'myProject'
        self.config = MagicMock(spec=Config)
        self.config.has_http_proxy.return_value = False
        self.config.http_proxy.return_value = ""
        self.utils = MagicMock(spect=Utils)
        self.cache = MagicMock(spec=PackageCache)

        def activate_path():
            return [os.path.join('home', 'code', 'activate.bash')][:]

        self.utils.get_activate_script_command.side_effect = activate_path

    @patch('subprocess.call')
    def test_will_run_pip_inside_virtualenvWhenInsideEnv(self, mock_subprocess):
        self.pip = PipRunner(self.config, self.utils)
        self.pip.install('dem')
        command = self.utils.get_activate_script_command()
        command.extend(['&&', 'pip', 'install', 'dem'])
        mock_subprocess.assert_called_with(command)

    @patch('subprocess.call')
    def test_will_remove_specified_no_version(self, mock_subprocess):
        self.pip = PipRunner(self.config, self.utils)
        self.pip.remove('dem', 'latest')

        mock_subprocess.assert_called_with(
            self.utils.get_activate_script_command() + ['&&', 'pip', 'uninstall', '--yes', 'dem'])

    @patch('subprocess.call')
    def test_will_remove_version_specified(self, mock_subprocess):
        self.pip = PipRunner(self.config, self.utils)
        self.pip.remove('dem', '0.5.9')

        mock_subprocess.assert_called_with(
            self.utils.get_activate_script_command() + ['&&', 'pip', 'uninstall', '--yes', 'dem==0.5.9'])

    @patch('subprocess.call')
    def test_will_install_version_specified(self, mock_subprocess):
        self.pip = PipRunner(self.config, self.utils)
        self.pip.install('dem', '0.5.9')

        mock_subprocess.assert_called_with(
            self.utils.get_activate_script_command() + ['&&', 'pip', 'install', 'dem==0.5.9'])

    @patch('subprocess.call')
    def test_will_install_version_specified_with_proxy(self, mock_subprocess):
        self.pip = PipRunner(self.config, self.utils)
        self.config.has_http_proxy.return_value = True
        self.config.http_proxy.return_value = 'http://11.2.3.1:900'
        self.pip.install('dem', '0.5.9')

        mock_subprocess.assert_called_with(
            self.utils.get_activate_script_command() + ['&&', 'pip', '--proxy=http://11.2.3.1:900', 'install',
                                                        'dem==0.5.9'])

    @patch('dem.dependency.pip.PipRunner.install')
    def test_will_install_packages_not_in_cache(self, mock_installer):
        self.cache.is_package_installed.return_value = False
        packages = [{'name': 'package', 'version': '1.3.0'},
                    {'name': 'package4', 'version': '0.3.0'}]
        pip_installer = PipInstaller(packages, self.config, self.cache, self.utils)
        packages, pip_installer.install_packages()

        mock_installer.assert_any_call('package', '1.3.0')
        mock_installer.assert_any_call('package4', '0.3.0')

    @patch('dem.dependency.pip.PipRunner.install')
    def test_will_not_install_packages_in_cache(self, mock_installer):
        def is_installed(package, version):
            if package == 'package':
                return True
            return False

        self.cache.is_package_installed.side_effect = is_installed;
        packages = [{'name': 'package', 'version': '1.3.0'},
                    {'name': 'package4', 'version': '0.3.0'}]
        pip_installer = PipInstaller(packages, self.config, self.cache, self.utils)
        pip_installer.install_packages()

        mock_installer.assert_called_once_with('package4', '0.3.0')


if __name__ == '__main__':
    unittest.main()
