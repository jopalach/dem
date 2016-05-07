import unittest
import mock
from dem.RpmInstaller import RpmInstaller
from dem.DevEnvReader import Config


class MyTestCase(unittest.TestCase):
    @mock.patch('subprocess.call')
    def test_will_install_package_with_yum_if_not_found_in_remote(self, mock_subprocess):
        packages = [{'name': 'package', 'version': '1.3.0'}]
        installer = RpmInstaller(packages)
        installer.install_packages()

        mock_subprocess.assert_called_once_with(['sudo', 'yum', 'install', 'package-1.3.0', '-y'])

    @mock.patch('subprocess.call')
    def test_will_install_all_packages_correctly(self, mock_subprocess):
        packages = [{'name': 'package', 'version': '1.3.0'},
                    {'name': 'package4', 'version': '0.3.0'}]
        installer = RpmInstaller(packages)
        installer.install_packages()

        mock_subprocess.assert_any_call(['sudo', 'yum', 'install', 'package-1.3.0', '-y'])
        mock_subprocess.assert_any_call(['sudo', 'yum', 'install', 'package4-0.3.0', '-y'])

if __name__ == '__main__':
    unittest.main()
