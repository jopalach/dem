from setuptools import setup

with open('README.rst') as f:
    readme = f.read()

setup(
    name="dem",
    version="0.0.4",
    author="Ian Macaulay, Jeremy Opalach",
    author_email="ismacaul@gmail.com",
    url="http://www.github.com/nitehawck/dem",
    description="An agnostic library/package manager for setting up a development project environment",
    long_description=readme,
    license="MIT License",
    classifiers=[
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        #'Development Status :: 5 - Production / Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Build Tools',
    ],
    packages=['dem'],
    install_requires=[
        'virtualenv',
        'PyYaml',
        'wget',
        'gitpython'
    ],
    tests_require=[
        'pyfakefs',
        'mock'
    ]
)