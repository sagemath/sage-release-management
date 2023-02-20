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
        Use the 's: positive review' label
        """
        for label in self.pr.labels:
            log.debug(f'pr {self.pr.number} label: {label.name}')
            if label.name == 's: positive review':
                return True
        return False

        
        # """
        # Need at least one approve, and no pending change request
        # """
        # approved = False
        # for review in self.pr.get_reviews():
        #     log.debug(f'considering review {review.state}: {review}')
        #     if review.state == 'REQUEST_CHANGES':
        #         return False
        #     approved = approved or (review.state == 'APPROVED')
        # log.debug(f'pr {self.pr.number} positive review: {approved}')
        # return approved

    
