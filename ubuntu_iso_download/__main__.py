# This file is part of ubuntu-iso-download. See LICENSE for license infomation.
"""Ubuntu ISO Download main module."""

import argparse
import logging
import sys

from . import url
from .iso import ISO

URLS = {
    'desktop': url.Desktop,
    'server': url.Server,
    'budgie': url.Budgie,
    'kubuntu': url.Kubuntu,
    'kylin': url.Kylin,
    'lubuntu': url.Lubuntu,
    'mate': url.Mate,
    'studio': url.Studio,
    'xubuntu': url.Xubuntu,
}


def parse_args():
    """Set up command-line arguments."""
    parser = argparse.ArgumentParser('ubuntu-iso')

    parser.add_argument(
        'flavor',
        choices=sorted(URLS.keys()),
        help='flavor name'
    )
    parser.add_argument(
        'codename',
        nargs='?',
        default=None,
        help='Ubuntu release codename (default: latest LTS release)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='do not download and only show link to ISO'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='additional logging output'
    )
    parser.add_argument(
        '--mirror',
        default='',
        help=(
            'mirror for supported desktop and server releases; '
            'see https://launchpad.net/ubuntu/+cdmirrors'
        )
    )

    return parser.parse_args()


def setup_logging(debug):
    """Set up logging.

    Args:
        debug: boolean, if additional logging
    """
    logging.basicConfig(
        stream=sys.stdout,
        format='%(message)s',
        level=logging.DEBUG if debug else logging.INFO
    )


def launch():
    """Launch ubuntu-iso-download."""
    args = parse_args()
    setup_logging(args.debug)

    iso = ISO(URLS[args.flavor], args.codename, mirror=args.mirror)
    print(iso)

    if args.dry_run:
        print(iso.target.url)
        sys.exit()

    iso.download()


if __name__ == '__main__':
    sys.exit(launch())
