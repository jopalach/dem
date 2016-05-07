import os, shutil
import virtualenv


class EnvironmentBuilder(object):
    @staticmethod
    def build(project):
        project_dir = os.path.join(os.getcwd(), '.devenv', project)
        if os.path.exists(project_dir):
            return

        print('[dem] building environment')
        deps_dir = os.path.join(project_dir, 'dependencies')

        os.makedirs(project_dir)
        virtualenv.create_environment(project_dir)
        os.makedirs(deps_dir)
