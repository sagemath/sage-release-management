import logging
from functools import cached_property
from typing import Final

from github.PullRequest import PullRequest

log = logging.getLogger('git-sage')


class SagePullRequest(object):

    def __init__(self, pr: PullRequest) -> None:
        self.pr: Final[PullRequest] = pr

    @cached_property
    def is_positive_review(self) -> bool:
        """
        Need at least one approve, and no pending change request
        """
        approved = False
        for review in self.pr.get_reviews():
            if review.state == 'REQUEST_CHANGES':
                return False
            approved = approved or (review.state == 'APPROVED')
        return approved

    
