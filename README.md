This is the official script used by the Sage Release Manager to manage the Sage release process.

## Install

    make install

## Test

    make lint
    make test

## Config 

Add ``config.yaml`` containing

    repository: "sagemath/sage"
    access_token: github_pat_xxxyyyzzz

### Use

    git-sage todo
    git-sage merge 12345 67890
