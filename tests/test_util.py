import os
from datetime import date
from unittest.mock import patch

from songmgr.util.util import get_config_file_path, str_to_date

from .helper import TestCaseWithTempDir


class TestUtil(TestCaseWithTempDir):

    def test_str_to_date(self):
        result = str_to_date('2010-10-10')
        expected = date(2010, 10, 10)
        self.assertEqual(result, expected)

    def test_get_config_file_path(self):
        with patch.dict('os.environ', {'HOME': self.temp_dir}):
            path = get_config_file_path('test.cfg')
        expected = os.path.join(self.temp_dir, '.songmgr', 'test.cfg')
        self.assertEqual(path, expected)
        self.assertTrue(os.path.isdir(os.path.join(self.temp_dir, '.songmgr')))
