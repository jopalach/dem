import os, shutil
import virtualenv


class EnvironmentBuilder(object):
    @staticmethod
    def build(project):
        env_dir = os.path.join(os.getcwd(), '.devenv')
        if os.path.exists(env_dir):
            shutil.rmtree(env_dir)

        project_dir = os.path.join(env_dir, project)
        deps_dir = os.path.join(project_dir, 'dependencies')

        os.makedirs(project_dir)
        virtualenv.create_environment(project_dir)
        os.makedirs(deps_dir)
