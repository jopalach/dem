import os
import unittest
import mock

from dem.DevEnvReader import Config
from dem.cache import PackageCache
from dem.UrlInstaller import UrlInstaller


class MyTestCase(unittest.TestCase):
    @mock.patch('wget.download')
    def test_will_get_packages_and_download(self, mock_wget):
        cache = mock.MagicMock(spec = PackageCache)
        packages = [{'name': 'package', 'version': '1.3.0', 'url': 'http://website.com/something.tar.gz'},
                    {'name': 'package4', 'version': '0.3.0', 'url': 'http://website.com/somethingElse.tar.gz'}]
        installer = UrlInstaller('myProject', packages, cache)

        mock_wget.download.return_value = 'file'
        installer.install_packages()

        download_file1 = os.path.join('.devenv', 'myProject', 'downloads', 'package-1.3.0.tar.gz')
        download_file2 = os.path.join('.devenv', 'myProject', 'downloads', 'package4-0.3.0.tar.gz')
        mock_wget.assert_any_call(packages[0]['url'], out=download_file1)
        mock_wget.assert_any_call(packages[1]['url'], out=download_file2)

    @mock.patch('os.path.exists')
    @mock.patch('wget.download')
    def test_will_not_download_if_exists_in_downloads(self, mock_wget, mock_exists):
        cache = mock.MagicMock(spec = PackageCache)
        packages = [{'name': 'package', 'version': '1.3.0', 'url': 'http://website.com/something.tar.gz'},
                    {'name': 'package4', 'version': '0.3.0', 'url': 'http://website.com/somethingElse.tar.gz'}]

        installer = UrlInstaller('myProject', packages, cache)

        mock_wget.download.return_value = 'file'
        download_file2 = os.path.join('.devenv', 'myProject', 'downloads', 'package4-0.3.0.tar.gz')

        def side_effect(file):
            if file == download_file2:
                return False
            return True
        mock_exists.side_effect = side_effect
        installer.install_packages()

        download_file2 = os.path.join('.devenv', 'myProject', 'downloads', 'package4-0.3.0.tar.gz')
        mock_wget.assert_called_once_with(packages[1]['url'], out=download_file2)

    # @mock.patch('os.path.exists')
    # @mock.patch('dem.ArchiveInstaller')
    # @mock.patch('wget.download')
    # def test_will_install_downloaded_packages(self, mock_wget, mock_archive_installer, mock_exists):
    #     packages = [{'name': 'package', 'version': '1.3.0', 'url': 'http://website.com/something.tar.gz'},
    #                 {'name': 'package4', 'version': '0.3.0', 'url': 'http://website.com/somethingElse.tar.gz'}]
    #
    #     mock_exists.return_value = False
    #     installer = UrlInstaller('myProject', packages)
    #
    #     print "hi"
    #     installer.install_packages()
    #
    #     expected_config = Config({'remote_locations:', os.path.join('.devenv', 'myProject', 'downloads')})
    #     mock_archive_installer.assert_called_once_with('myProject', expected_config, packages)


if __name__ == '__main__':
    unittest.main()
