# This file is part of ubuntu-iso. See LICENSE for license infomation.
"""Ubuntu ISO module."""

import argparse
import logging
import sys

FLAVORS = [
    'core',
    'desktop',
    'netboot',
    'server',
    # https://www.ubuntu.com/download/flavours
    'budgie',
    'kubuntu',
    'kylin',
    'lubuntu',
    'mate',
    'studio',
    'xubuntu'
]


def parse_args():
    """Set up command-line arguments."""
    parser = argparse.ArgumentParser('ubuntu-iso')

    parser.add_argument(
        'codename',
        help='Ubuntu release codename (e.g. bionic, xenial)'
    )
    parser.add_argument(
        'flavor', choices=FLAVORS,
        help='flavor name'
    )
    parser.add_argument(
        '--arch',
        choices=['amd64', 'arm64', 'i386', 'ppc64el', 's390x'],
        default='amd64',
        help='architecture of image (default: amd64)'
    )
    parser.add_argument(
        '--daily', action='store_true',
        help='download the latest daily image'
    )
    parser.add_argument(
        '--dry-run', action='store_true',
        help='do not download and only show link to ISO'
    )
    parser.add_argument(
        '--debug', action='store_true',
        help='additional logging output'
    )

    return parser.parse_args()


def setup_logging(debug):
    """Set up logging."""
    logging.basicConfig(
        stream=sys.stdout,
        format='%(message)s',
        level=logging.DEBUG if debug else logging.INFO
    )


def launch():
    """Launch ubuntu-iso."""
    args = parse_args()
    setup_logging(args.debug)

    print(
        'user wants %s %s %s' % (args.release, args.flavor, args.arch)
    )
    if args.daily:
        print('daily image')
    if args.dry_run:
        print('dry run set')


if __name__ == '__main__':
    sys.exit(launch())
