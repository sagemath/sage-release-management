import logging
from itertools import islice
from math import inf
from typing import Final, List

from git_sage.github.sage_github import SageGithub
from git_sage.repo.sage_repository import SageRepository

log = logging.getLogger('git-sage')


class MergeCommand(object):

    def __init__(self, sage: SageRepository, github: SageGithub) -> None:
        self.sage: Final[SageRepository] = sage
        self.github: Final[SageGithub] = github

    def _merge_specific_pr_numbers(self, pr_numbers: List[int]) -> None:
        for pr_number in pr_numbers:
            spr = self.github.get_pull(pr_number)
            if not spr.is_positive_review:
                raise ValueError(f'pr {pr_number} does not have positive review')
            print(f'Merging {spr.pr}')
            self.sage.merge_pr(spr.pr)

    def _merge_all(self, limit: int) -> None:
        for spr in islice(self.github.pull_requests(None), limit):
            if not spr.is_positive_review:
                continue
            print(f'Merging {spr.pr}')
            self.sage.merge_pr(spr.pr)
        
    def __call__(self, pr_numbers: List[int], limit: int) -> None:
        if pr_numbers:
            self._merge_specific_pr_numbers(pr_numbers)
        else:
            self._merge_all(limit)
