import os
from abc import ABCMeta, abstractmethod


class Config(object, metaclass=ABCMeta):

    def __init__(self, config_file_path):
        super().__init__()
        self.file_path = config_file_path
        if os.path.isfile(config_file_path):
            with open(config_file_path) as f:
                self._read_lines(f)

    def save(self, file_path=None):
        file_path = file_path or self.file_path
        with open(file_path, 'w') as f:
            self._write_lines(f)

    @abstractmethod
    def _read_lines(self, f):
        pass

    @abstractmethod
    def _write_lines(self, f):
        pass


class DictConfig(Config, dict):

    def _read_lines(self, f):
        for line in f:
            key, value = line.rstrip().split(':')
            self[key] = value

    def _write_lines(self, f):
        for key, value in self.items():
            line = '{}:{}\n'.format(key, value)
            f.write(line)


class SetConfig(Config, set):

    def _read_lines(self, f):
        for line in f:
            self.add(line.rstrip())

    def _write_lines(self, f):
        for item in sorted(self):
            f.write(item + '\n')


CONFIG_TYPES = {'dict': DictConfig, 'set': SetConfig}
