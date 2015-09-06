import distutils.cmd


import setuptools.command.build_py
from setuptools import setup, find_packages


class BuildWithLintCommand(setuptools.command.build_py.build_py):
    """Custom build command."""

    def run(self):
        self.run_command('lint')
        setuptools.command.build_py.build_py.run(self)


setup(
    name="python-multi*",
    version="1.0",
    description="Example of using multiprocessing and multithread library",
    author="Andreea Lucau",
    author_email="andreea.lucau@gmail.com",
    url="https://github.com/andreea-lucau/python-multithread-multiprocess",
    packages=find_packages("src"),
    package_dir = {
        "": "src",
    },
    install_requires=[
        "setuptools",
        "setuptools-lint",
        "Sphinx"
    ],
    #cmdclass={
    #    'build_py': BuildWithLintCommand,
    #},
)
