import os

from . import ArchiveInstaller
from . import DevEnvReader as reader


def get_dem_packages():
    (config, packages) = reader.devenv_from_file('devenv.yaml')

    os.makedirs('devenv')

    archive_installer = ArchiveInstaller.ArchiveInstaller(config, packages)
    archive_installer.install_packages()
