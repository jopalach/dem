import os

from . ArchiveInstaller import ArchiveInstaller
from . import DevEnvReader as reader
from . EnvironmentBuilder import EnvironmentBuilder
from . RpmInstaller import RpmInstaller
from . PackageCache import PackageCache

def get_dem_packages(project):
    (config, packages) = reader.devenv_from_file('devenv.yaml')

    cache = PackageCache(os.getcwd())
    if not cache.needs_update():
        print('[dem] Up to date.')
        return

    EnvironmentBuilder.build(project)

    archive_installer = ArchiveInstaller(project, config, packages)
    archive_installer.install_packages()

    rpm_installer = RpmInstaller(packages.rpm_packages())
    rpm_installer.install_packages()

    cache.update()

if __name__ == '__main__':
    project = os.path.basename(os.getcwd())
    get_dem_packages(project)
