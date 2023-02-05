import logging
from typing import Final

from git_sage.config.config import GitSageConfig

log = logging.getLogger('git-sage')



class SageRepository(object):

    def __init__(self,
                 config: GitSageConfig
                 ) -> None:
        self.config: Final[GitSageConfig] = config
