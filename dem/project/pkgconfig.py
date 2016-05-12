import os


class PkgConfigProcessor(object):
    @staticmethod
    def replace_prefix(locations, pkg_config):
        for loc in locations:
            pkg_config_path = os.path.join(loc, pkg_config.replace('/', os.sep))
            if os.path.exists(pkg_config_path):
                pkg_config_files = [f for f in os.listdir(pkg_config_path) if f.endswith('.pc')]
                for pkg_config_file in pkg_config_files:
                    pkg_config_file_path = os.path.join(pkg_config_path, pkg_config_file)
                    with open(pkg_config_file_path) as f:
                        contents = f.readlines()
                    with open(pkg_config_file_path, 'w+') as f:
                        for line in contents:
                            if line.startswith('prefix='):
                                loc = loc.replace(os.sep, '/')
                                f.write('prefix={}\n'.format(loc))
                            else:
                                f.write(line)




