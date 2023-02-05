import logging
import os
import unittest

from git_sage.config.config import GitSageConfig
from git_sage.config.loader import config_file_path, config_loader

basedir = os.path.dirname(os.path.dirname(__file__))

log = logging.getLogger('git-sage.test')

class TestConfigLoader(unittest.TestCase):
    
    def test_config_loader(self) -> None:
        config_yaml = config_file_path()
        config = config_loader(config_yaml)
        print(config)
