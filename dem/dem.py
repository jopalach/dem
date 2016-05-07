import os

from dem.ArchiveInstaller import ArchiveInstaller
import dem.DevEnvReader as reader
from dem.EnvironmentBuilder import EnvironmentBuilder
from dem.RpmInstaller import RpmInstaller


def get_dem_packages(project):
    (config, packages) = reader.devenv_from_file('devenv.yaml')

    EnvironmentBuilder.build(project)

    archive_installer = ArchiveInstaller(project, config, packages)
    archive_installer.install_packages()

    rpm_installer = RpmInstaller(packages.rpm_packages())
    rpm_installer.install_packages()

if __name__ == '__main__':
    project = os.path.basename(os.getcwd())
    get_dem_packages(project)
