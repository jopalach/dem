import unittest
import mock
from dem.RpmInstaller import RpmInstaller
from dem.DevEnvReader import Config

class MyTestCase(unittest.TestCase):

    @mock.patch('os.path.join')
    @mock.patch('os.path.exists')
    @mock.patch('subprocess.call')
    def test_will_install_rpms_if_found_in_remote_location(self, mock_subprocess, mock_exists, mock_join):
        mock_exists.return_value = True
        mock_join.return_value = '/remote/repo/package'

        config = Config({'remote_locations': ['/remote/repo']})
        packages = [{'name': 'package', 'version': '1.3.0'}]
        installer = RpmInstaller('project', config, packages)
        installer.install_packages()

        mock_subprocess.assert_called_once_with(['rpm', '-i', '/remote/repo/package-1.3.0.rpm'])

    @mock.patch('os.path.join')
    @mock.patch('os.path.exists')
    @mock.patch('subprocess.call')
    def test_will_install_rpm_found_in_first_remote(self, mock_subprocess, mock_exists, mock_join):
        mock_exists.side_effect = [False, True, True]
        mock_join.side_effect = ['/remote/repo/package', '/remote/repo2/package', '/remote/repo3/package']

        config = Config({'remote_locations': ['/remote/repo', '/remote/repo2', '/remote/repo3']})
        packages = [{'name': 'package', 'version': '1.3.0'}]
        installer = RpmInstaller('project', config, packages)
        installer.install_packages()

        mock_subprocess.assert_called_once_with(['rpm', '-i', '/remote/repo2/package-1.3.0.rpm'])

    @mock.patch('os.path.join')
    @mock.patch('os.path.exists')
    @mock.patch('subprocess.call')
    def test_will_install_package_with_yum_if_not_found_in_remote(self, mock_subprocess, mock_exists, mock_join):
        mock_exists.return_value = False
        mock_join.side_effect = ['/remote/repo/package', '/remote/repo2/package']

        config = Config({'remote_locations': ['/remote/repo', '/remote/repo2']})
        packages = [{'name': 'package', 'version': '1.3.0'}]
        installer = RpmInstaller('project', config, packages)
        installer.install_packages()

        mock_subprocess.assert_called_once_with(['sudo', 'yum', 'install', 'package-1.3.0', '-y'])


    @mock.patch('os.path.join')
    @mock.patch('os.path.exists')
    @mock.patch('subprocess.call')
    def test_will_install_all_packages_correctly(self, mock_subprocess, mock_exists, mock_join):
        mock_exists.side_effect = [False, False,
                                   True,
                                   False, True,
                                   False, False]
        mock_join.side_effect = ['/remote/repo/package', '/remote/repo2/package',
                                 '/remote/repo/package2',
                                 '/remote/repo/package3', '/remote/repo2/package3',
                                 '/remote/repo/package4', '/remote/repo2/package4']

        config = Config({'remote_locations': ['/remote/repo', '/remote/repo2']})
        packages = [{'name': 'package', 'version': '1.3.0'},
                    {'name': 'package2', 'version': '2.3.0'},
                    {'name': 'package3', 'version': '3.3'},
                    {'name': 'package4', 'version': '0.3.0'}]
        installer = RpmInstaller('project', config, packages)
        installer.install_packages()

        mock_subprocess.assert_any_call(['sudo', 'yum', 'install', 'package-1.3.0', '-y'])
        mock_subprocess.assert_any_call(['rpm', '-i', '/remote/repo/package2-2.3.0.rpm'])
        mock_subprocess.assert_any_call(['rpm', '-i', '/remote/repo2/package3-3.3.rpm'])
        mock_subprocess.assert_any_call(['sudo', 'yum', 'install', 'package4-0.3.0', '-y'])

if __name__ == '__main__':
    unittest.main()
