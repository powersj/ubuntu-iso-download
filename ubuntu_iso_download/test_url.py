# This file is part of ubuntu-iso-download. See LICENSE file for license info.
"""Test url module."""
import pytest

from .url import (
    Budgie,
    Desktop,
    Kubuntu,
    Kylin,
    Lubuntu,
    Mate,
    Netboot,
    Server,
    Studio,
    URL,
    Xubuntu,
)


class Release:
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


XENIAL = Release("xenial", False, True, "16.04", 4, 16)
BIONIC = Release("bionic", False, True, "18.04", 4, 18)
DISCO = Release("disco", True, False, "19.04", 4, 19)


def test_url():
    """Test basic URL."""
    arch = "amd64"
    release = BIONIC

    url = URL(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ""
    assert str(url) == "Unknown ISO on %s" % release
    assert url.hash_file == (
        "http://cdimage.ubuntu.com/Unknown/releases/" "bionic/release/SHA256SUMS"
    )
    assert url.hash_file_signed == (
        "http://cdimage.ubuntu.com/Unknown/releases/" "bionic/release/SHA256SUMS.gpg"
    )


def test_mirror():
    """Test customized mirror."""
    arch = "ppc64el"
    release = DISCO
    mirror = "http://mirror.wiru.co.za/ubuntu-releases/"

    url = URL(release, arch, mirror)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == "http://mirror.wiru.co.za/ubuntu-releases"
    assert str(url) == "Unknown ISO on %s" % release


def test_mirror_netboot():
    """Test customized mirror."""
    arch = "amd64"
    release = DISCO
    mirror = "http://mirror.wiru.co.za/ubuntu-releases"

    url = Netboot(release, arch, mirror)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == "http://mirror.wiru.co.za/ubuntu-releases"
    assert str(url) == "Ubuntu Netboot ISO on %s" % release


def test_desktop_stable():
    """Test desktop stable url."""
    arch = "amd64"
    release = BIONIC

    url = Desktop(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ""
    assert str(url) == "Ubuntu Desktop ISO on %s" % release
    assert url.url == ("http://releases.ubuntu.com/18.04")


def test_desktop_devel():
    """Test desktop devel url."""
    arch = "amd64"
    release = DISCO

    url = Desktop(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ""
    assert str(url) == "Ubuntu Desktop ISO on %s" % release
    assert url.url == ("http://cdimage.ubuntu.com/ubuntu/" "daily-live/current")


def test_server_stable_old():
    """Pre-18.04 server ISO."""
    arch = "amd64"
    release = XENIAL

    url = Server(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ""
    assert str(url) == "Ubuntu Server ISO on %s" % release
    assert url.url == ("http://releases.ubuntu.com/16.04")


def test_server_stable():
    """Test stable server url."""
    arch = "amd64"
    release = BIONIC

    url = Server(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ""
    assert str(url) == "Ubuntu Server ISO on %s" % release
    assert url.url == ("http://releases.ubuntu.com/18.04")


def test_server_devel():
    """Test devel server url."""
    arch = "amd64"
    release = DISCO

    url = Server(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ""
    assert str(url) == "Ubuntu Server ISO on %s" % release
    assert url.url == ("http://cdimage.ubuntu.com/ubuntu-server/daily-live/current")


def test_netboot_stable():
    """Test stable netboot url."""
    arch = "amd64"
    release = BIONIC

    url = Netboot(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ""
    assert str(url) == "Ubuntu Netboot ISO on %s" % release
    assert url.url == (
        "http://archive.ubuntu.com/ubuntu/dists/bionic/main/"
        "installer-amd64/current/images"
    )


def test_netboot_devel():
    """Test devel netboot url."""
    arch = "i386"
    release = DISCO

    url = Netboot(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert url.mirror == ""
    assert str(url) == "Ubuntu Netboot ISO on %s" % release
    assert url.url == (
        "http://archive.ubuntu.com/ubuntu/dists/disco/main/"
        "installer-i386/current/images"
    )


def test_netboot_ppc64el():
    """Test devel netboot on bad arch."""
    arch = "ppc64el"
    release = DISCO

    with pytest.raises(SystemExit):
        Netboot(release, arch)


def test_budgie_stable():
    """Test budgie stable url."""
    arch = "amd64"
    release = BIONIC

    url = Budgie(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Ubuntu Budgie ISO on %s" % release


def test_budgie_devel():
    """Test budgie devel url."""
    arch = "amd64"
    release = DISCO

    url = Budgie(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Ubuntu Budgie ISO on %s" % release


def test_budgie_unsupported():
    """Test budgie unsupported release."""
    arch = "amd64"
    release = XENIAL

    with pytest.raises(SystemExit):
        Budgie(release, arch)


def test_kubuntu_stable():
    """Test kubuntu stable url."""
    arch = "amd64"
    release = BIONIC

    url = Kubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Kubuntu ISO on %s" % release


def test_kubuntu_devel():
    """Test kubuntu devel url."""
    arch = "amd64"
    release = DISCO

    url = Kubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Kubuntu ISO on %s" % release


def test_kylin_stable():
    """Test kylin stable url."""
    arch = "amd64"
    release = BIONIC

    url = Kylin(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Ubuntu Kylin ISO on %s" % release


def test_kylin_devel():
    """Test kylin devel url."""
    arch = "amd64"
    release = DISCO

    url = Kylin(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Ubuntu Kylin ISO on %s" % release


def test_lubuntu_stable():
    """Test lubuntu stable url."""
    arch = "amd64"
    release = BIONIC

    url = Lubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Lubuntu ISO on %s" % release


def test_lubuntu_devel():
    """Test lubuntu devel url."""
    arch = "amd64"
    release = DISCO

    url = Lubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Lubuntu ISO on %s" % release


def test_mate_stable():
    """Test mate stable url."""
    arch = "amd64"
    release = BIONIC

    url = Mate(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Ubuntu MATE ISO on %s" % release


def test_mate_devel():
    """Test mate devel url."""
    arch = "amd64"
    release = DISCO

    url = Mate(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Ubuntu MATE ISO on %s" % release


def test_studio_stable():
    """Test studio stable url."""
    arch = "amd64"
    release = BIONIC

    url = Studio(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Ubuntu Studio ISO on %s" % release


def test_studio_devel():
    """Test studio devel url."""
    arch = "amd64"
    release = DISCO

    url = Studio(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Ubuntu Studio ISO on %s" % release
    assert url.url == ("http://cdimage.ubuntu.com/ubuntustudio/dvd/current")


def test_xubuntu_stable():
    """Test xubuntu stable url."""
    arch = "amd64"
    release = BIONIC

    url = Xubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Xubuntu ISO on %s" % release


def test_xubuntu_devel():
    """Test xubuntu devel rul."""
    arch = "amd64"
    release = DISCO

    url = Xubuntu(release, arch)
    assert url.arch == arch
    assert url.release == release
    assert str(url) == "Xubuntu ISO on %s" % release
