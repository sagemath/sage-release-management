import logging
from functools import cached_property
from typing import Final, List

from git_sage.repo.wrap_lines import wrap_lines
from git_sage.util.uniq import uniq
from github.NamedUser import NamedUser
from github.PullRequest import PullRequest
from pygit2 import Branch, Commit, Remote, Repository

log = logging.getLogger('git-sage')


TEMPLATE = """
gh-pr-{number}: {title}
    
{description}
    
URL: {url}
Reported by: {user}
Reviewer(s): {reviewers}
"""


def user_name(user: NamedUser) -> str:
    return user.name or user.login


class MergeConflictException(Exception):
    pass


class ReleaseMerge(object):

    def __init__(self,
                 repo: Repository,
                 github: Remote,
                 pr: PullRequest,
                 ) -> None:
        self.repo: Final[Repository] = repo
        self.github: Final[Remote] = github
        self.pr: Final[PullRequest] = pr

    @cached_property
    def reviewer_names(self) -> List[str]:
        """
        Ordered and deduplicated reviewer names
        """
        deduplicated = uniq(
            user_name(review.user) for review in self.pr.get_reviews())
        return sorted(deduplicated, key=lambda name: name.lower())
        
    @cached_property
    def message(self) -> str:
        print(self.pr)
        return TEMPLATE.format(
            number=self.pr.number,
            title=self.pr.title,
            description=wrap_lines(self.pr.body),
            url=self.pr.html_url,
            user=user_name(self.pr.user),
            reviewers=', '.join(self.reviewer_names),
        )

    # @cached_property
    # def branch(self) -> Branch:
    #     number = self.pr.number
    #     name = f'refs/pull/{number}/head'
    #     log.debug(f'pr branch name should be {name}')
    #     branch = self.repo.branches.get(name)
    #     if not branch:
    #         raise ValueError(f'branch {name} not found')
    #     return branch

    @property
    def branch_tip(self) -> Commit:
        number = self.pr.number
        name = f'refs/pull/{number}/head'
        log.debug(f'pr branch name should be {name}')
        self.github.fetch([name])
        return self.repo.revparse_single('FETCH_HEAD')
    
        # print(origin.fetch_refspecs)
        # print(origin.fetch())
        # print(dir(origin))
        # print(origin.fetch_refspecs)
        # print(origin.refspec_count)
        # print(origin.get_refspec(0).src)
        # print(origin.get_refspec(0).dst)
        # print(dir(origin.get_refspec(0)))
        # # print(origin.ls_remotes())
        # print(dir(origin))
        # print(self.repo.lookup_reference_dwim('refs/remotes/origin/develop'))
        # name = f'refs/remotes/origin/pull/{number}/head'
        # log.debug(f'pr ref name should be {name}')
        # ref = self.repo.lookup_reference_dwim(name)
        # if not ref:
        #     raise ValueError(f'pr ref {name} not found')
        # return ref

    def merge_commit(self) -> Commit:
        """
        Add the release commit to the repository, and return the merge commit
        """
        branch_tip = self.branch_tip.oid
        self.repo.merge(branch_tip)
        user = self.repo.default_signature
        tree = self.repo.index.write_tree()
        message = self.message
        merge_commit = self.repo.create_commit(
            'HEAD', user, user, message, tree,
            [self.repo.head.target, branch_tip])
        if self.repo.index.conflicts:
            raise MergeConflictException(self.pr.number)
        self.repo.state_cleanup()
        return merge_commit
