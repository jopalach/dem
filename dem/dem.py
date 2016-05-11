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
from .utils import Utils
from .piprunner import PipInstaller

def get_dem_packages(project):
    utils = Utils(project)
    base_path = utils.get_project_root_path()

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

    pip_installer = PipInstaller(packages.pip_packages(), config, cache, utils)
    installed_packages.extend(pip_installer.install_packages())

    cache.update(installed_packages)


def main():
    project = os.path.basename(os.getcwd())
    get_dem_packages(project)


if __name__ == '__main__':
    main()

