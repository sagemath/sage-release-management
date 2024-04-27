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
        Use the 's: positive review' and 's: needs work' labels
        """
        is_needs_work = False
        is_positive_review = False
        for label in self.pr.labels:
            log.debug(f'pr {self.pr.number} label: {label.name}')
            is_positive_review = is_positive_review or (label.name == 's: positive review')
            is_needs_work = is_needs_work or (label.name == 's: needs work')
        return is_positive_review and not is_needs_work

    @cached_property
    def is_blocker(self) -> bool:
        """
        Use the 's: blocker / 1' label
        """
        is_blocker = False
        for label in self.pr.labels:
            log.debug(f'pr {self.pr.number} label: {label.name}')
            is_blocker = is_blocker or (label.name == 'p: blocker / 1')
        return is_blocker

        
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

    
