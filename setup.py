from setuptools import setup
import os

scripts_dir = 'scripts'
scripts = [os.path.join(scripts_dir, file_name) for file_name in os.listdir(scripts_dir)]


setup(
    name='songmgr',
    version='0.2.0',
    packages=['songmgr'],
    scripts=scripts,
)
