import datetime
import os

from .config import DictConfig


def create_directory_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def get_config_file_path(filename):
    config_dir = os.path.join(os.environ['HOME'], '.songmgr')
    create_directory_if_not_exists(config_dir)
    return os.path.join(config_dir, filename)


def relative_path(location):
    config = DictConfig(get_config_file_path('favourite_song.cfg'))
    return os.path.relpath(os.path.realpath(location), config['music_dir']).replace('\\', '/')


def str_to_date(x):
    return datetime.datetime.strptime(x, '%Y-%m-%d').date()
