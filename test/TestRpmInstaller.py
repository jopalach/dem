import unittest
import mock
from dem.RpmInstaller import RpmInstaller
from dem.cache import PackageCache


class MyTestCase(unittest.TestCase):
    @mock.patch('subprocess.call')
    def test_will_install_package_with_yum_if_not_found_in_remote(self, mock_subprocess):
        cache = mock.MagicMock(spec=PackageCache)
        cache.is_package_installed.return_value = False
        packages = [{'name': 'package', 'version': '1.3.0'}]
        installer = RpmInstaller(packages, cache)
        installer.install_packages()

        mock_subprocess.assert_called_once_with(['sudo', 'yum', 'install', 'package-1.3.0', '-y'])

    @mock.patch('subprocess.call')
    def test_will_install_all_packages_correctly(self, mock_subprocess):
        cache = mock.MagicMock(spec=PackageCache)
        cache.is_package_installed.return_value = False
        packages = [{'name': 'package', 'version': '1.3.0'},
                    {'name': 'package4', 'version': '0.3.0'}]
        installer = RpmInstaller(packages, cache)
        installer.install_packages()

        mock_subprocess.assert_any_call(['sudo', 'yum', 'install', 'package-1.3.0', '-y'])
        mock_subprocess.assert_any_call(['sudo', 'yum', 'install', 'package4-0.3.0', '-y'])

    @mock.patch('subprocess.call')
    def test_will_not_install_rpm_if_already_installed(self, mock_subprocess):
        cache = mock.MagicMock(spec=PackageCache)
        cache.is_package_installed.return_value = True
        packages = [{'name': 'package', 'version': '1.3.0'},
                    {'name': 'package4', 'version': '0.3.0'}]
        installer = RpmInstaller(packages, cache)
        installer.install_packages()
        mock_subprocess.assert_not_called()


if __name__ == '__main__':
    unittest.main()
