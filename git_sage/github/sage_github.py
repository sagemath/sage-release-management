import logging
from functools import cached_property
from typing import Final, Iterable, List, Optional

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
    
    def pull_requests(self, limit: Optional[int], only_blocker: bool) -> Iterable[SagePullRequest]:
        pulls = self.repo.get_pulls(
            state='open',
            sort='created',
            direction='asc',
        )
        count: int = 0
        for pr in pulls:
            if (limit is not None) and (count >= limit):
                return
            spr = SagePullRequest(pr)
            if only_blocker and not spr.is_blocker:
                continue
            yield spr
            count += 1

    def print_table(self, limit: int, only_blocker: bool) -> None:
        table = PullRequestTable(self.pull_requests(limit, only_blocker))
        table.stream_print()
