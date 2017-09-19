import os
import shutil
from unittest import TestCase


class TestCaseWithTempDir(TestCase):

    def setUp(self):
        self.test_files = os.path.join(os.path.dirname(__file__), 'test_files')
        self.temp_dir = os.path.join(self.test_files, 'temp')
        os.mkdir(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)
