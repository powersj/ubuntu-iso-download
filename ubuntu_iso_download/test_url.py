# This file is part of ubuntu-iso-download. See LICENSE file for license info.
"""Test url module."""
import pytest

from .url import (
    Budgie, Desktop, Kubuntu, Kylin, Lubuntu, Mate,
    Server, Studio, URL, Xubuntu
)


class Release():
    """Dummy release class."""

    def __init__(self, codename, is_dev, lts, version, month, year):
        """Initialize release class."""
        self.codename = codename
        self.is_dev = is_dev
        self.lts = lts
        self.month = month
        self.version = version
        self.year = year

    def __repr__(self):
        return self.codename


XENIAL = Release('xenial', False, True, '16.04', 4, 16)
BIONIC = Release('bionic', False, True, '18.04', 4, 18)
DISCO = Release('disco', True, False, '19.04', 4, 19)


def test_url():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = URL(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ''
    assert str(url) == 'Unknown ISO on %s' % release
    assert url.hash_file == (
        'http://cdimage.ubuntu.com/Unknown/releases/'
        'bionic/release/SHA256SUMS'
    )
    assert url.hash_file_signed == (
        'http://cdimage.ubuntu.com/Unknown/releases/'
        'bionic/release/SHA256SUMS.gpg'
    )


def test_mirror():
    """TODO."""
    arch = 'ppc64el'
    release = DISCO
    mirror = 'http://mirror.wiru.co.za/ubuntu-releases/'

    url = URL(release, arch, mirror)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == 'http://mirror.wiru.co.za/ubuntu-releases'
    assert str(url) == 'Unknown ISO on %s' % release


def test_desktop_stable():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = Desktop(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ''
    assert str(url) == 'Ubuntu Desktop ISO on %s' % release
    assert url.url == (
        'http://releases.ubuntu.com/18.04/ubuntu-18.04-desktop-amd64.iso'
    )


def test_desktop_devel():
    """TODO."""
    arch = 'amd64'
    release = DISCO

    url = Desktop(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ''
    assert str(url) == 'Ubuntu Desktop ISO on %s' % release
    assert url.url == (
        'http://cdimage.ubuntu.com/ubuntu/'
        'daily-live/current/disco-desktop-amd64.iso'
    )


def test_server_stable_old():
    """Pre-18.04."""
    arch = 'amd64'
    release = XENIAL

    url = Server(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ''
    assert str(url) == 'Ubuntu Server ISO on %s' % release
    assert url.url == (
        'http://releases.ubuntu.com/16.04/ubuntu-16.04-server-amd64.iso'
    )


def test_server_stable():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = Server(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ''
    assert str(url) == 'Ubuntu Server ISO on %s' % release
    assert url.url == (
        'http://releases.ubuntu.com/18.04/ubuntu-18.04-live-server-amd64.iso'
    )


def test_server_devel():
    """TODO."""
    arch = 'amd64'
    release = DISCO

    url = Server(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ''
    assert str(url) == 'Ubuntu Server ISO on %s' % release
    assert url.url == (
        'http://cdimage.ubuntu.com/ubuntu-server/'
        'daily-live/current/disco-live-server-amd64.iso'
    )


def test_budgie_stable():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = Budgie(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Ubuntu Budgie ISO on %s' % release


def test_budgie_devel():
    """TODO."""
    arch = 'amd64'
    release = DISCO

    url = Budgie(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Ubuntu Budgie ISO on %s' % release


def test_budgie_unsupported():
    """TODO."""
    arch = 'amd64'
    release = XENIAL

    with pytest.raises(SystemExit):
        Budgie(release, arch)


def test_kubuntu_stable():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = Kubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Kubuntu ISO on %s' % release


def test_kubuntu_devel():
    """TODO."""
    arch = 'amd64'
    release = DISCO

    url = Kubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Kubuntu ISO on %s' % release


def test_kylin_stable():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = Kylin(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Ubuntu Kylin ISO on %s' % release


def test_kylin_devel():
    """TODO."""
    arch = 'amd64'
    release = DISCO

    url = Kylin(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Ubuntu Kylin ISO on %s' % release


def test_lubuntu_stable():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = Lubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Lubuntu ISO on %s' % release


def test_lubuntu_devel():
    """TODO."""
    arch = 'amd64'
    release = DISCO

    url = Lubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Lubuntu ISO on %s' % release


def test_mate_stable():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = Mate(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Ubuntu MATE ISO on %s' % release


def test_mate_devel():
    """TODO."""
    arch = 'amd64'
    release = DISCO

    url = Mate(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Ubuntu MATE ISO on %s' % release


def test_studio_stable():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = Studio(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Ubuntu Studio ISO on %s' % release


def test_studio_devel():
    """TODO."""
    arch = 'amd64'
    release = DISCO

    url = Studio(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Ubuntu Studio ISO on %s' % release
    assert url.url == (
        'http://cdimage.ubuntu.com/ubuntustudio'
        '/dvd/current/disco-dvd-amd64.iso'
    )


def test_xubuntu_stable():
    """TODO."""
    arch = 'amd64'
    release = BIONIC

    url = Xubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Xubuntu ISO on %s' % release


def test_xubuntu_devel():
    """TODO."""
    arch = 'amd64'
    release = DISCO

    url = Xubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == 'Xubuntu ISO on %s' % release
