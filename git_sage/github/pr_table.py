import logging
from functools import cached_property
from typing import Final, Iterable, List

from beautifultable import BeautifulTable
from git_sage.github.sage_pr import SagePullRequest

log = logging.getLogger('git-sage')


class PullRequestTable(object):

    def __init__(self, pulls: Iterable[SagePullRequest]) -> None:
        self.pulls: Final[Iterable[SagePullRequest]] = pulls

    @cached_property
    def table(self) -> BeautifulTable:
        table = BeautifulTable()
        table.set_style(BeautifulTable.STYLE_DOTTED)
        table.columns.header = ['Number', 'Review', 'Title']
        table.columns.width = [8, 10, 40]
        table.columns.width_exceed_policy = BeautifulTable.WEP_ELLIPSIS
        return table

    def _format(self, spr: SagePullRequest) -> List[str]:
        return [
            str(spr.pr.number),
            'approved' if spr.is_positive_review else '',
            spr.pr.title,
        ]
    
    def _lines(self) -> Iterable[List[str]]:
        for pr in self.pulls:
            yield self._format(pr)
    
    def stream_print(self) -> None:
        for line in self.table.stream(self._lines()):
            print(line)
