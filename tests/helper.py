import os
from unittest import TestCase


class TestCaseWithTempFiles(TestCase):

    def setUp(self):
        self.temp_files = []
        self.test_files = os.path.join(os.path.dirname(__file__), 'test_files')

    def tearDown(self):
        for file_path in self.temp_files:
            if os.path.exists(file_path):
                os.remove(file_path)
