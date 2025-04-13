from setuptools import setup, find_packages

setup(
    name='Research-ChatBot',
    version='0.1',
    packages=find_packages(where="src"),
    install_requires=[],
    package_dir={"": "src"},
)