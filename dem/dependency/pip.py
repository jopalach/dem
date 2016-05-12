import subprocess


class PipRunner(object):
    def __init__(self, config, util):
        self.util = util
        self.config = config

    def install(self, package, version='latest'):
        self._execute_pip_command(package, version, 'install')

    def remove(self, package, version='latest'):
        self._execute_pip_command(package, version, 'remove')

    def _add_remove_pip(self):
        command = ['&&', 'pip', 'uninstall', '--yes']
        return command

    def _add_install_pip(self):
        command = ['&&', 'pip']
        if self.config is not None and self.config.has_http_proxy():
            command.extend(['--proxy={}'.format(self.config.http_proxy())])
        command.extend(['install'])
        return command

    def _execute_pip_command(self, package, version, action):
        command = self.util.get_activate_script_command()
        if action == 'install':
            command.extend(self._add_install_pip())
        else:
            command.extend(self._add_remove_pip())

        if version == 'latest':
            subprocess.call(command + [package])
        else:
            subprocess.call(command + ['{}=={}'.format(package, version)])


class PipInstaller(object):
    def __init__(self, packages, config, cache, util):
        self.util = util
        self.config = config
        self.cache = cache
        self.packages = packages
        self.pip_runner = PipRunner(config, util)

    def install_packages(self):
        installed_packages = []
        for p in self.packages:
            if self.cache.is_package_installed(p['name'], p['version']):
                print('[dem] {}-{} already installed'.format(p['name'], p['version']))
            else:
                print('[dem] pip installing {}-{}'.format(p['name'], p['version']))
                self.pip_runner.install(p['name'], p['version'])
                package = dict()
                package[p['name']] = {'version': p['version'], 'type': 'pip'}
                installed_packages.append(package)

        return installed_packages
