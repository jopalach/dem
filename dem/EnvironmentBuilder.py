import os
import virtualenv


class EnvironmentBuilder(object):
    @staticmethod
    def create(project):
        env_dir = os.path.join(os.getcwd(), '.devenv')
        project_dir = os.path.join(env_dir, project)
        deps_dir = os.path.join(project_dir, 'dependencies')

        os.makedirs(project_dir)
        virtualenv.create_environment(project_dir)
        os.makedirs(deps_dir)
