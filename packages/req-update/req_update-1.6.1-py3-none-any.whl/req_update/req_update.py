#!/usr/bin/env python3

from __future__ import annotations
import argparse
import os
import subprocess
import sys
from typing import Set

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import node  # NOQA
import python  # NOQA
import util  # NOQA


VERSION = (1, 6, 1)
__version__ = '.'.join(map(str, VERSION))


DESCRIPTION = (
    'Update python dependencies for your project with git integration\n'
    'https://github.com/albertyw/req-update'
)


def main() -> None:
    ReqUpdate().main()


class ReqUpdate():
    def __init__(self) -> None:
        self.install = False
        self.updated_files: Set[str] = set([])
        self.util = util.Util()
        self.python = python.Python()
        self.python.util = self.util
        self.node = node.Node()
        self.node.util = self.util

    def main(self) -> None:
        """ Update all dependencies """
        self.get_args()
        branch_created = False
        self.util.check_repository_cleanliness()
        if self.python.check_applicable():
            if not branch_created:
                self.util.create_branch()
                branch_created = True
            self.python.update_install_dependencies()
        if self.node.check_applicable():
            if not branch_created:
                self.util.create_branch()
                branch_created = True
            self.node.update_install_dependencies()

    def get_args(self) -> argparse.Namespace:
        parser = argparse.ArgumentParser(description=DESCRIPTION)
        parser.add_argument(
            '-p',
            '--push',
            action='store_true',
            help='Push commits individually to remote origin',
        )
        parser.add_argument(
            '-i',
            '--install',
            action='store_true',
            help='Install updates',
        )
        parser.add_argument(
            '-d',
            '--dryrun',
            action='store_true',
            help='Dry run',
        )
        parser.add_argument(
            '-v',
            '--verbose',
            action='store_true',
            help='Verbose output',
        )
        parser.add_argument(
            '--version',
            action='version',
            version=__version__,
        )
        args = parser.parse_args()
        self.install = args.install
        self.util.push = args.push
        self.util.verbose = args.verbose
        self.util.dry_run = args.dryrun
        return args


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError:
        pass
