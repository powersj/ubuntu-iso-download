# This file is part of ubuntu-iso-download. See LICENSE for license infomation.
"""Ubuntu ISO Download Release class.

Similar to the 'distro-info' package, this class parses and contains
the Ubuntu release information. Instead of a static data file, this
instead downloads the the meta-release information from
changelogs.ubuntu.com. This information is parsed to determine all the
release information.
"""

import logging
from operator import attrgetter
import sys

import requests
import yaml

logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)


class UbuntuRelease:
    """UbuntuRelease object.

    Contains the meta-data information for a particular Ubuntu release.
    """

    def __init__(self, codename, name, version, supported, lts=False):
        """Create an UbuntuRelease Object.

        Args:
            codename: string, single word, lower-case (e.g. bionic)
            name: string, full, multi-word name (e.g. Bionic Beaver LTS)
            version: string, like 'YY.MM[.#] [LTS]' (e.g. '18.04.1 LTS')
            supported: boolean, if supported or not
            lts: boolean, if LTS or not
        """
        self.codename = codename
        self.name = name
        self.version = version.replace(' LTS', '')
        self.is_supported = supported
        self.is_lts = lts
        self.is_dev = False

    def __eq__(self, other):
        """Return equality boolean."""
        if not isinstance(other, UbuntuRelease):
            return False

        if self.version == other.version:
            return True

        return False

    def __ge__(self, other):
        """Return greater than or equal boolean."""
        if self.year < other.year:
            return False
        elif self.year > other.year:
            return True
        elif self.month < other.month:
            return False
        elif self.month > other.month:
            return False
        elif self.point < other.point:
            return False
        elif self.point > other.point:
            return True

        return True

    def __gt__(self, other):
        """Return greater than boolean."""
        if self.year < other.year:
            return False
        elif self.year > other.year:
            return True
        elif self.month < other.month:
            return False
        elif self.month > other.month:
            return False
        elif self.point < other.point:
            return False
        elif self.point > other.point:
            return True

        return False

    def __le__(self, other):
        """Return less than or equal boolean."""
        return not self.__ge__(other)

    def __lt__(self, other):
        """Return less than boolean."""
        return not self.__gt__(other)

    def __ne__(self, other):
        """Return not equal boolean."""
        if not isinstance(other, UbuntuRelease):
            return False

        return not self.__eq__(other)

    def __repr__(self):
        """Return formal string of release."""
        if self.is_lts:
            return '%s LTS' % self.version

        return self.version

    @property
    def year(self):
        """Return year of release."""
        return int(self.version.split('.')[0])

    @property
    def month(self):
        """Return month of release."""
        return int(self.version.split('.')[1])

    @property
    def point(self):
        """Return point of release."""
        try:
            return int(self.version.split('.')[2])
        except IndexError:
            return 0


class UbuntuReleaseData:
    """UbuntuReleaseData Object."""

    url_release = 'https://changelogs.ubuntu.com/meta-release'
    url_release_dev = 'https://changelogs.ubuntu.com/meta-release-development'

    def __init__(self):
        """Initialize object.

        This set of classes build Ubuntu release information based on the
        meta-data found in https://changelogs.ubuntu.com/. Essentially, the
        meta-release file is read that contains all the released, past and
        present releases, with flags as to support status.

        The meta-release-development file is used to determine what the current
        development release is.
        """
        self._log = logging.getLogger(__name__)
        self.releases = self._parse_meta_url(self.url_release)

        # now find the development release and add it as supported
        dev_releases = self._parse_meta_url(self.url_release_dev)
        for codename, release in dev_releases.items():
            if codename not in self.releases:
                release.is_dev = True
                release.is_supported = True
                self.releases[codename] = release

    def _parse_meta_url(self, url):
        """Parse meta-data from URL and return releases found.

        Exits if unable to download from URL.

        Args:
            url: url to get meta-data from

        Returns:
            dictionary of releases, codename as key

        """
        releases = {}

        meta_data = requests.get(url)
        if not meta_data.ok:
            self._log.error(
                'Oops: could not download Ubuntu meta-release from: %s', url
            )
            sys.exit(1)

        for release in meta_data.content.decode('utf-8').split('\n\n'):
            # use the baseloader to prevent it from munging the version
            # from a string to some odd integer value
            data = yaml.load(release, Loader=yaml.BaseLoader)

            supported = False
            if data['Supported'] == '1':
                supported = True

            lts = False
            if 'LTS' in data['Version']:
                lts = True

            releases[data['Dist']] = UbuntuRelease(
                data['Dist'], data['Name'], data['Version'], supported, lts
            )

        return releases

    def by_codename(self, codename):
        """Return release given a specific codename.

        Exits on unknown release.

        Args:
            codename: string of codename to find

        Returns:
            UbuntuRelease object of matching release

        """
        try:
            return self.releases[codename]
        except KeyError:
            self._log.error(
                'Oops: unknown release codename \'%s\'!'
                ' Please choose from:\n%s',
                codename, [release.codename for release in self.supported])
            sys.exit(1)

    @property
    def all(self):
        """Return all releases.

        Return:
            List of all UbuntuRelease objects.

        """
        return self.releases

    @property
    def devel(self):
        """Return devel release.

        Return:
            UbuntuRelease object that is devel, or None.

        """
        for _, release in self.releases.items():
            if release.is_devel:
                return release

        return None

    @property
    def lts(self):
        """Return latest LTS.

        Returns:
            UbuntuRelease object that is the latest LTS.

        """
        lts = []
        for _, release in self.releases.items():
            if release.is_lts and not release.is_dev:
                lts.append(release)

        return max(lts, key=attrgetter('year'))

    @property
    def stable(self):
        """Return latest stable release.

        Returns:
            UbuntuRelease object that is the stable release.

        """
        supported = []
        for _, release in self.releases.items():
            if release.is_supported and not release.is_dev:
                supported.append(release)

        return max(supported)

    @property
    def supported(self):
        """Return supported releases.

        Returns:
            List of UbuntuRelease objects that are supported.

        """
        supported = []
        for _, release in self.releases.items():
            if release.is_supported:
                supported.append(release)

        return supported
