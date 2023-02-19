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
        type=int,
        help='Limit number of PRs', 
        default=10)
    
    parser_merge = subparsers.add_parser(
        'merge',
        help='merge pull requests')
    parser_merge.add_argument(
        '-l', '--limit',
        dest='limit', 
        type=int,
        help='Auto-merge this many outstanding PRs', 
        default=0)
    parser_merge.add_argument(
        'pr_number',
        nargs='*',
        type=int,
        help='Number(s) of Github PR to merge', 
        default=[]
    )
    
    # subparsers = parser.add_subparsers(
    #     dest='subparser',
    #     help='sub-command help')
    return parser
