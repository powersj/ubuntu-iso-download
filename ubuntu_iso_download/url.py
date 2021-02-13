# This file is part of ubuntu-iso-download. See LICENSE for license infomation.
"""Ubuntu ISO Download URL class.

This is used to generate a URL for a specific flavor and release of
Ubuntu (desktop or server) or any recognized flavor. The flavors list
is initially based on the list found at the following:

    https://www.ubuntu.com/download/flavours

Supported and development release ISOs are kept in different locations
and use different names due to the fact that the development release
name (e.g. 18.10) is not set until the release.

Ubuntu Desktop and Server AMD64 ISOs are kept on 'release.ubuntu.com',
whereas flavors, development release, and other architectures are kept
on 'cdimage.ubuntu.com'.

Due to simplicity and demand, this only creates URLs for AMD64 (x86_64)
ISOs.
"""

import logging
import sys

ENOENT_URL = """Oops: URL not found
If you are sure this is not networking related AND know the ISO exists
would you please file a bug and let us know that the following:
 * flavor: %s
 * release: %s
 * arch: %s
 * url: %s"""

URL_ARCHIVE = "http://archive.ubuntu.com"
URL_CDIMAGE = "http://cdimage.ubuntu.com"
URL_RELEASES = "http://releases.ubuntu.com"


class URL:
    """Base URL.

    Base URL class to establish most of the usual names and parameters.
    Sub-classes can override individual URL and filenames as necessary
    to allow for unique situations (e.g. non-LTS releases, different
    filenames, etc.).
    """

    flavor = "Unknown"
    name = "Unknown"
    variety = "desktop"

    def __init__(self, release, arch="amd64", mirror=""):
        """Initialize base URL."""
        self._log = logging.getLogger(__name__)

        self.arch = arch
        self.release = release
        self.mirror = mirror.strip("/")

    def __repr__(self):
        """Return string representation of ISO."""
        return "%s ISO on %s" % (self.name, self.release)

    @property
    def hash_file(self):
        """Return URL to hash file."""
        return "%s/SHA256SUMS" % self.url

    @property
    def hash_file_signed(self):
        """Return URL to signed hash file."""
        return "%s/SHA256SUMS.gpg" % self.url

    @property
    def url(self):
        """Return URL to ISO."""
        url = self._supported_url()
        if self.release.is_dev:
            url = self._development_url()

        return url

    def _development_url(self):
        """Return the development url."""
        return "{base_url}/{flavor}/{path}".format(
            base_url=URL_CDIMAGE, flavor=self.flavor, path="daily-live/current",
        )

    def _supported_url(self):
        """Return supported release url."""
        return "{base_url}/{flavor}/{path}".format(
            base_url=URL_CDIMAGE,
            flavor=self.flavor,
            path="releases/{codename}/release".format(codename=self.release.codename),
        )


class Server(URL):
    """Ubuntu Server."""

    name = "Ubuntu Server"
    flavor = "ubuntu-server"
    variety = "live-server"

    def __init__(self, release, arch="amd64", mirror=""):
        """Initialize Server object.

        The released versions's flavor is 'ubuntu' instead of
        'ubuntu-server'.

        The server ISO before 18.04 was based on the Debian Installer
        (d-i). After 18.04, it uses subiquity and is known as
        'server-live'.
        """
        super().__init__(release, arch, mirror)

        if not self.release.is_dev:
            self.flavor = "ubuntu"

        if self.release.year < 18:
            self.variety = "server"

    def _supported_url(self):
        """Return supported release url."""
        return "{base_url}/{version}".format(
            base_url=self.mirror if self.mirror else URL_RELEASES,
            version=self.release.version,
        )


class Desktop(URL):
    """Ubuntu Desktop."""

    name = "Ubuntu Desktop"
    flavor = "ubuntu"

    def _supported_url(self):
        """Return supported release url."""
        return "{base_url}/{version}".format(
            base_url=self.mirror if self.mirror else URL_RELEASES,
            version=self.release.version,
        )


class Netboot(URL):
    """Ubuntu Netboot."""

    name = "Ubuntu Netboot"
    flavor = "netboot"
    variety = "mini"

    def __init__(self, release, arch="amd64", mirror=""):
        """Initialize Netboot object.

        Netboot is only supported on amd64 and i386, before 20.04.
        """
        super().__init__(release, arch, mirror)
        supported_arch = ["amd64", "i386"]

        if self.arch not in supported_arch:
            self._log.error("The Ubuntu netboot is only supported on amd64 and i386.")
            sys.exit(1)

        if self.release.year >= 20:
            self._log.error("The netboot ISO was discontinued after 19.10.")
            sys.exit(1)

    @property
    def dir(self):
        """Return URL of ISO directory that has the GPG keys."""
        return "/".join(self.url.split("/")[:-2])

    @property
    def url(self):
        """Return URL to ISO."""
        return (
            "{base_url}/ubuntu/dists/{release}/main/installer-{arch}"
            "/current/images".format(
                base_url=self.mirror if self.mirror else URL_ARCHIVE,
                release=self.release,
                arch=self.arch,
            )
        )


class Budgie(URL):
    """Budgie Desktop Flavor."""

    name = "Ubuntu Budgie"
    flavor = "ubuntu-budgie"

    def __init__(self, release, arch="amd64", mirror=""):
        """Initialize Budgie object.

        Budgie was not supported until the 18.04 LTS.
        """
        super().__init__(release, arch, mirror)

        if self.release.year < 18:
            self._log.error(
                "The Ubuntu Budgie flavor was not supported until the 18.04 release"
            )
            sys.exit(1)


class Kubuntu(URL):
    """Kubuntu Desktop Flavor."""

    name = "Kubuntu"
    flavor = "kubuntu"


class Kylin(URL):
    """Kylin Desktop Flavor."""

    name = "Ubuntu Kylin"
    flavor = "ubuntukylin"


class Lubuntu(URL):
    """Lubuntu Desktop Flavor."""

    name = "Lubuntu"
    flavor = "lubuntu"


class Mate(URL):
    """Mate Desktop Flavor."""

    name = "Ubuntu MATE"
    flavor = "ubuntu-mate"


class Studio(URL):
    """Studio Desktop Flavor."""

    name = "Ubuntu Studio"
    flavor = "ubuntustudio"
    variety = "dvd"

    def __init__(self, release, arch="amd64", mirror=""):
        """Initialize Studio object.

        The 18.04 release was not known as an LTS release.
        """
        super().__init__(release, arch, mirror)

        if self.release.year == 18 and self.release.month == 4:
            self._log.debug("18.04 was not an LTS for Ubuntu Studio.")
            self.release.lts = False
            self.release.version = "18.04"

    def _development_url(self):
        """Return the development url."""
        return "{base_url}/{flavor}/{path}".format(
            base_url=URL_CDIMAGE, flavor=self.flavor, path="%s/current" % self.variety,
        )


class Xubuntu(URL):
    """Xubuntu Desktop Flavor."""

    name = "Xubuntu"
    flavor = "xubuntu"
