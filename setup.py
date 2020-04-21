from setuptools import find_packages, setup

INSTALL_REQUIRES = [
    'sqlalchemy',
    'flask',
    'requests',
    'flask-wtf',
    'flask-admin',
    'flask-login',
    'flask-classy'
]

DEV_REQUIRES = [
    'rope',
    'pytest',
    'autopep8',
    'pylint'
]

ENTRY_POINTS = {
    'console_scripts': [
        'ypd_server=ypd.scripts.server:main',
        'init_db=ypd.scripts.initialize_database:main',
    ]
}

setup(
    name="ycp_project_database",
    version="0.0.1",
    packages=find_packages("src"),
    author='abaldwin3, creynolds1, gholley, llewis9',
    description = "Python Server for project_proposer",
    install_requires = INSTALL_REQUIRES,
    extra_require = {
        "dev": DEV_REQUIRES
    },
    package_dir={'': 'src'},
    entry_points=ENTRY_POINTS
)
