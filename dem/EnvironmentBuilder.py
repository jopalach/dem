import os
import virtualenv


def create_dem_env():
    dem_env = os.path.join(os.getcwd(), 'demenv')
    python_dir = os.path.join(dem_env, 'python')
    dependencies_dir = os.path.join(dem_env, 'libs')

    os.makedirs(python_dir)
    os.makedirs(dependencies_dir)

    virtualenv.create_environment(python_dir)



