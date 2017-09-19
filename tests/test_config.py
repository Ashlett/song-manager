import os

from songmgr.util.config import DictConfig, SetConfig

from .helper import TestCaseWithTempDir


class TestConfig(TestCaseWithTempDir):

    def setUp(self):
        super().setUp()
        self.test_config = os.path.join(self.temp_dir, 'test.cfg')

    def test_dict_config(self):
        dict_config = DictConfig(self.test_config)
        dict_config['key'] = 'value'
        self.assertFalse(os.path.isfile(self.test_config))
        dict_config.save()
        self.assertTrue(os.path.isfile(self.test_config))
        with open(self.test_config) as f:
            content = f.read()
        self.assertEqual(content, 'key:value\n')
        del dict_config
        dict_config = DictConfig(self.test_config)
        self.assertEqual(dict_config['key'], 'value')

    def test_set_config(self):
        set_config = SetConfig(self.test_config)
        set_config.add('element1')
        set_config.add('element2')
        self.assertFalse(os.path.isfile(self.test_config))
        set_config.save()
        self.assertTrue(os.path.isfile(self.test_config))
        with open(self.test_config) as f:
            content = f.read()
        self.assertEqual(content, 'element1\nelement2\n')
        del set_config
        set_config = SetConfig(self.test_config)
        self.assertEqual(set_config, {'element1', 'element2'})
