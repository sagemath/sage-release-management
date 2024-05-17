import logging
import sys

from git_sage.cmdline.application import Application
from git_sage.cmdline.logger import log
from git_sage.cmdline.parser import cmdline_parser


def main() -> None:
    parser = cmdline_parser()
    args = parser.parse_args(sys.argv[1:])
    print(args)
    if args.log is not None:
        level = getattr(logging, args.log)
        log.setLevel(level=level)
    # logging.basicConfig(level=logging.DEBUG)
    app = Application()
    if args.subcommand == 'todo':
        app.todo_cmd(args.limit, args.only_blocker)
    if args.subcommand == 'merge':
        app.merge_cmd(args.pr_number, args.exclude, args.limit, args.only_blocker)
