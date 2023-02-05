import argparse
import logging
import sys

log = logging.getLogger('git-sage')


description = '''
Sage Release Management CLI
'''


def cmdline_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--log', dest='log', default=None,
        help='one of [DEBUG, INFO, ERROR, WARNING, CRITICAL]')
    subparsers = parser.add_subparsers(
        dest='subcommand')
    parser_todo = subparsers.add_parser(
        'todo',
        help='list pull requests that are ready to merge')
    parser_todo.add_argument(
        '-l', '--limit',
        dest='limit', 
        help='Limit number of PRs', 
        default=10)
    # subparsers = parser.add_subparsers(
    #     dest='subparser',
    #     help='sub-command help')
    return parser
