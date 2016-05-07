import os

from . ArchiveInstaller import ArchiveInstaller
from . import DevEnvReader as reader
from . EnvironmentBuilder import EnvironmentBuilder
from . RpmInstaller import RpmInstaller
from . cache import PackageCache
from . uninstaller import PackageUninstaller
from . UrlInstaller import UrlInstaller


def get_dem_packages(project):
    (config, packages) = reader.devenv_from_file('devenv.yaml')

    cache = PackageCache(os.getcwd())
    if not cache.needs_update():
        print('[dem] Up to date.')
        return

    EnvironmentBuilder.build(project)

    package_uninstaller = PackageUninstaller(cache, packages)
    package_uninstaller.uninstall_changed_packages()

    archive_installer = ArchiveInstaller(project, config, packages.archive_packages(), cache)
    installed_packages = archive_installer.install_packages()

    rpm_installer = RpmInstaller(packages.rpm_packages(), cache)
    installed_packages.extend(rpm_installer.install_packages())

    url_installer = UrlInstaller(project, packages.url_packages(), cache)
    installed_packages.extend(url_installer.install_packages())

    cache.update(installed_packages)

if __name__ == '__main__':
    project = os.path.basename(os.getcwd())
    get_dem_packages(project)
