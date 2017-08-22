import datetime

import os

from .config import CONFIG_TYPES


def create_directory_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def get_config_file_path(filename):
    config_dir = os.path.join(os.environ['HOME'], '.songmgr')
    create_directory_if_not_exists(config_dir)
    return os.path.join(config_dir, filename)


def get_config(filename, config_type='dict'):
    config_class = CONFIG_TYPES[config_type]
    return config_class(get_config_file_path(filename))


def str_to_date(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d').date()
