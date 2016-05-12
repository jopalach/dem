import os, shutil, errno, stat

import sys


class Utils(object):
    def __init__(self, project_name):
        self.project_name = project_name

    @staticmethod
    def remove_directory(path):
        shutil.rmtree(path, ignore_errors=False, onerror=remove_read_only)

    def get_project_root_path(self):
        if not os.path.exists('devenv.yaml') and 'VIRTUAL_ENV' not in os.environ:
            print('[dem] Please run from project root or enter the virtual environment to be able to run from anywhere')
            sys.exit(1)
        elif os.path.exists('devenv.yaml') and 'VIRTUAL_ENV' not in os.environ:
            return os.getcwd()
        elif 'SKIP_ENVIRONMENT_CHECK' in os.environ:  # Tests run in a virtual environment!
            return os.getcwd()
        else:
            return os.environ['VIRTUAL_ENV'].split(os.path.join('.devenv'), 1)[0]

    def get_virtual_env_project_path(self):
        return os.path.join(self.get_project_root_path(), '.devenv', self.project_name)

    def get_activate_script_command(self):
        if sys.platform == 'win32':
            bin = 'Scripts'
            exe = 'activate.bat'
        else:
            bin = 'bin'
            exe = 'activate.bash'

        cmd = [os.path.join(self.get_virtual_env_project_path(), bin, exe)]
        return cmd[:]


# http://stackoverflow.com/questions/1213706/what-user-do-python-scripts-run-as-in-windows
def remove_read_only(func, path, exc):
    excvalue = exc[1]
    path_as_list = get_list(path)
    for index, val in enumerate(path_as_list):
        if val.startswith('.') and val != '.devenv':
            print("Encountered an error deleting: {}\nAttempting to fix...".format(path))
            val = 'soonToBeDeleted'
            dir_path = os.path.join(*path_as_list[0:index])
            dir_path = os.path.join(dir_path, val)
            os.rename(path, dir_path)  # 0777
            if sys.platform == 'win32':
                # http://www.thecodingforums.com/threads/removing-hidden-files-and-folders-with-python.588249/
                os.system("attrib -r -h -s {}".format(dir_path))
                os.chmod(dir_path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
                func(dir_path)


# http://stackoverflow.com/questions/3167154/how-to-split-a-dos-path-into-its-components-in-python
def get_list(path):
    folders = []
    while 1:
        path, folder = os.path.split(path)
        if folder != "":
            folders.append(folder)
        else:
            if path != "":
                folders.append(path)
            folders.reverse()
            return folders
