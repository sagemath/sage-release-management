import logging
from functools import cached_property
from typing import Final, List

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
        for pr_number in pr_numbers:
            spr = self.github.get_pull(pr_number)
            if not spr.is_positive_review:
                raise ValueError(f'pr {pr_number} does not have positive review')
            print(f'Merging {spr.pr}')
            self.sage.merge_pr(spr.pr)
        if not pr_numbers:
            for spr in self.github.pull_requests(limit):
                print(f'Merging {spr.pr}')
                self.sage.merge_pr(spr.pr)
