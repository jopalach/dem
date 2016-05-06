import os

import ArchiveInstaller
import DevEnvReader as reader
from EnvironmentBuilder import EnvironmentBuilder


def get_dem_packages(project):
    (config, packages) = reader.devenv_from_file('devenv.yaml')

    EnvironmentBuilder.build(project)

    archive_installer = ArchiveInstaller.ArchiveInstaller(config, packages)
    archive_installer.install_packages(project)


if __name__ == '__main__':
    project = os.path.basename(os.getcwd())
    get_dem_packages(project)
