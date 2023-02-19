import logging
from functools import cached_property
from typing import Final, Iterable, List

from git_sage.config.config import GitSageConfig
from git_sage.github.pr_table import PullRequestTable
from git_sage.github.sage_pr import SagePullRequest
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
        return self.gh.get_repo('sagemath/sage')  # 'vbraun/sage')

    def get_pull(self, pr_number: int) -> SagePullRequest:
        pr = self.repo.get_pull(pr_number)
        return SagePullRequest(pr)
    
    def pull_requests(self, limit: int) -> Iterable[SagePullRequest]:
        pulls = self.repo.get_pulls(
            state='open',
            sort='created',
            direction='asc',
        )
        count: int = 0
        for pr in pulls:
            if count >= limit:
                return
            yield SagePullRequest(pr)
            count += 1

    def print_table(self, limit: int) -> None:
        table = PullRequestTable(self.pull_requests(limit))
        table.stream_print()
