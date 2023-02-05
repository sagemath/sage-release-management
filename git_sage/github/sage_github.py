import logging
from functools import cached_property
from typing import Final, Iterable

from git_sage.config.config import GitSageConfig
from github import Github
from github.PullRequest import PullRequest
from github.Repository import Repository

log = logging.getLogger('git-sage')


class SageGithub(object):

    def __init__(self,
                 config: GitSageConfig
                 ) -> None:
        self.config: Final[GitSageConfig] = config

    @cached_property
    def gh(self) -> Github:
        return Github(self.config.access_token)

    @cached_property
    def repo(self) -> Repository:
        return self.gh.get_repo('sagemath/sage-archive-2023-02-01')  # 'vbraun/sage')

    def pull_requests(self) -> Iterable[PullRequest]:
        return self.repo.get_pulls(state='closed', sort='created')
