import logging
from functools import cached_property
from typing import Final, List

from git_sage.cmdline.merge_command import MergeCommand
from git_sage.config.config import GitSageConfig
from git_sage.config.loader import config_file_path, config_loader
from git_sage.github.sage_github import SageGithub
from git_sage.repo.sage_repository import SageRepository

log = logging.getLogger('git-sage')


class Application(object):

    def __init__(self) -> None:
        pass

    @cached_property
    def config(self) -> GitSageConfig:
        config_yaml = config_file_path()
        return config_loader(config_yaml)

    @cached_property
    def sage(self) -> SageRepository:
        return SageRepository(
            config=self.config,
        )

    @cached_property
    def github(self) -> SageGithub:
        return SageGithub(
            config=self.config,
        )

    def todo_cmd(self, limit: int) -> None:
        """
        Print the next open pull requests
        """
        self.github.print_table(limit)

    def merge_cmd(self, pr_numbers: List[int], limit: int) -> None:
        cmd = MergeCommand(self.sage, self.github)
        cmd(pr_numbers, limit)
