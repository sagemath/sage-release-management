import logging
from itertools import islice
from math import inf
from typing import Final, FrozenSet, List

from git_sage.github.sage_github import SageGithub
from git_sage.repo.release_merge import MergeConflictException
from git_sage.repo.sage_repository import SageRepository

log = logging.getLogger('git-sage')


class MergeCommand(object):

    def __init__(self, sage: SageRepository, github: SageGithub) -> None:
        self.sage: Final[SageRepository] = sage
        self.github: Final[SageGithub] = github

    def _merge_specific_pr_numbers(self, pr_numbers: List[int], force: bool) -> None:
        for pr_number in pr_numbers:
            spr = self.github.get_pull(pr_number)
            if not (force or spr.is_positive_review):
                raise ValueError(f'pr {pr_number} does not have positive review')
            print(f'Merging {spr.pr}')
            self.sage.merge_pr(spr.pr)

    def _merge_all(self,
                   limit: int,
                   exclude: FrozenSet[int],
                   only_blocker: bool) -> None:
        for spr in islice(self.github.pull_requests(None, only_blocker), limit):
            if spr.pr in exclude:
                continue
            if not spr.is_positive_review:
                continue
            print(f'Merging {spr.pr}')
            try:
                self.sage.merge_pr(spr.pr)
            except MergeConflictException as exc:
                print(f'Merge failed: {exc}')
        
    def __call__(self,
                 pr_numbers: list[int],
                 exclude: list[int],
                 limit: int,
                 only_blocker: bool,
                 ) -> None:
        exclude_set = frozenset(exclude)
        if pr_numbers:
            filtered = [pr for pr in pr_numbers if pr not in exclude_set]
            self._merge_specific_pr_numbers(filtered, True)
        else:
            self._merge_all(limit, exclude_set, only_blocker)
