import os

from git_sage.config.config import GitSageConfig
from yaml import Loader, load


def config_file_path() -> str:
    """
    Find the config file
    """
    basedir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    config_yaml = os.path.join(basedir, 'config.yaml')
    return config_yaml


def config_loader(filename: str) -> GitSageConfig:
    """
    Load the config file
    """
    with open(filename, 'r') as f:
        data = load(f, Loader=Loader)
    return GitSageConfig(
        repository=data['repository'],
        access_token=data['access_token'],
    )
