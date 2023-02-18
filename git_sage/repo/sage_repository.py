import logging
import os
from functools import cached_property
from typing import Final, Optional, cast

import pygit2
from git_sage.config.config import GitSageConfig
from git_sage.repo.release_merge import ReleaseMerge
from github.PullRequest import PullRequest
from pygit2 import Remote, RemoteCallbacks, Repository

log = logging.getLogger('git-sage')


class SageRepositoryException(Exception):
    pass


class SageRepository(object):

    def __init__(self,
                 config: GitSageConfig
                 ) -> None:
        self.config: Final[GitSageConfig] = config
        self._verify_remotes()

    @cached_property
    def callbacks(self) -> RemoteCallbacks:
        keypair = pygit2.KeypairFromAgent('git')
        callbacks = pygit2.RemoteCallbacks(credentials=keypair)
        return callbacks
        
    @cached_property
    def repo(self) -> Repository:
        path = self._path_from_local() or self._path_from_cwd()
        if not path:
            raise SageRepositoryException('sage git repo not found')
        repo = Repository(path)
        return repo

    def _path_from_cwd(self) -> Optional[str]:
        log.debug('searching sage repo in cwd')
        path = pygit2.discover_repository(os.getcwd())
        return cast(Optional[str], path)

    def _path_from_local(self) -> Optional[str]:
        repo_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        log.debug(f'searching sage repo in {repo_root}')
        sage_repo = os.path.join(repo_root, 'Sage')
        log.debug(f'using sage repo: {sage_repo}')
        path = pygit2.discover_repository(sage_repo)
        return cast(Optional[str], path)

    @cached_property
    def origin(self) -> Remote:
        try:
            return self.repo.remotes['origin']
        except KeyError:
            raise SageRepositoryException('origin remote not defined')

    @cached_property
    def github(self) -> Remote:
        try:
            return self.repo.remotes['github']
        except KeyError:
            raise SageRepositoryException('github remote not defined')
    
    def _verify_remotes(self) -> None:
        origin_url = ['git@github.com:vbraun/sage.git']
        github_url = ['git@github.com:sagemath/sage.git', 'https://github.com/sagemath/sage.git']
        if self.origin.url not in origin_url:
            raise SageRepositoryException(f'origin remote should be {origin_url}')
        if self.github.url not in github_url:
            raise SageRepositoryException(f'github remote should be {github_url}')

    def merge_pr(self, pr: PullRequest) -> None:
        release = ReleaseMerge(self.repo, self.github, self.callbacks, pr)
        release.merge_commit()

