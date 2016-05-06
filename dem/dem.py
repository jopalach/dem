import os

import ArchiveInstaller
import DevEnvReader as reader
from EnvironmentBuilder import EnvironmentBuilder
from RpmInstaller import RpmInstaller

def get_dem_packages(project):
    (config, packages) = reader.devenv_from_file('devenv.yaml')

    EnvironmentBuilder.build(project)

    archive_installer = ArchiveInstaller.ArchiveInstaller(project, config, packages)
    archive_installer.install_packages()

    rpm_installer = RpmInstaller(project, config, packages.rpm_packages())
    rpm_installer.install_packages()

if __name__ == '__main__':
    project = os.path.basename(os.getcwd())
    get_dem_packages(project)
