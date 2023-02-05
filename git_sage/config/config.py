from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class GitSageConfig(object):

    repository: str
    access_token: str
    
    
