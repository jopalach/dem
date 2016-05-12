import sys, os
import dem


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    project = os.path.basename(os.getcwd())
    dem.get_dem_packages(project)


if __name__ == '__main__':
    main()

