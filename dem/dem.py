import os

import sys

from . GitProjectInstaller import GitProjectInstaller
from . ArchiveInstaller import ArchiveInstaller
from . import DevEnvReader as reader
from . EnvironmentBuilder import EnvironmentBuilder
from . RpmInstaller import RpmInstaller
from . cache import PackageCache
from . uninstaller import PackageUninstaller
from . UrlInstaller import UrlInstaller


def get_dem_packages(project):
    if not os.path.exists('devenv.yaml') and 'VIRTUAL_ENV' not in os.environ:
        print('[dem] Please run from project root or enter the virtual environment to be able to run from anywhere')
        sys.exit(1)
    elif os.path.exists('devenv.yaml') and 'VIRTUAL_ENV' not in os.environ:
        base_path = os.getcwd()
    elif 'SKIP_ENVIRONMENT_CHECK' in os.environ:  # Tests run in a virtual environment!
        base_path = os.getcwd()
    else:
        base_path = os.environ['VIRTUAL_ENV'].split(os.path.join('.devenv'), 1)[0]

    (config, packages) = reader.devenv_from_file(os.path.join(base_path, 'devenv.yaml'))

    cache = PackageCache(project, base_path)
    if not cache.needs_update():
        print('[dem] Up to date.')
        return
    reader.fixup_packages(packages, cache)
    EnvironmentBuilder.build(project, config)

    package_uninstaller = PackageUninstaller(cache, packages)
    package_uninstaller.uninstall_changed_packages()

    archive_installer = ArchiveInstaller(project, config, packages.archive_packages(), cache)
    installed_packages = archive_installer.install_packages()

    rpm_installer = RpmInstaller(packages.rpm_packages(), cache)
    installed_packages.extend(rpm_installer.install_packages())

    url_installer = UrlInstaller(project, packages.url_packages(), cache)
    installed_packages.extend(url_installer.install_packages())

    git_installer = GitProjectInstaller(packages.git_packages(), cache)
    installed_packages.extend(git_installer.install_packages())

    cache.update(installed_packages)


def main():
    project = os.path.basename(os.getcwd())
    get_dem_packages(project)


if __name__ == '__main__':
    main()

