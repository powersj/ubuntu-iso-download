# This file is part of ubuntu-iso-download. See LICENSE for license infomation.
"""Ubuntu ISO Download ISO class.

This is the signing key used for Ubuntu CD Images:

    pub   rsa4096 2012-05-11 [SC]
    Ubuntu CD Image Automatic Signing Key (2012) <cdimage@ubuntu.com>
    843938DF228D22F7B3742BC0D94AA3F0EFE21092

It is found in the ubuntu-archive-keyring.gpg file of the
ubuntu-keyring package in the Ubuntu archive.

"""

import hashlib
import logging
import os
import sys
import tempfile

import gnupg
import requests
from tqdm import tqdm

from ubuntu_release_info import data as UbuntuReleaseInfo

logging.getLogger("gnupg").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)


class ISO:
    """Base ISO."""

    def __init__(self, flavor, release, mirror=None):
        """Initialize ISO class."""
        self._log = logging.getLogger(__name__)
        self.release = self.get_ubuntu_release(release)
        self.target = flavor(self.release, mirror=mirror)
        self.ubuntu_cd_public_gpg = self._read_gpg_key()

    def __repr__(self):
        """Return string representation of ISO."""
        return str(self.target)

    def _read_gpg_key(self):
        """Read the public GPG key used for signing CDs."""
        keyring_path = "usr/share/keyrings/ubuntu-archive-keyring.gpg"
        if os.getenv("SNAP"):
            keyring_path = os.path.join(os.getenv("SNAP"), keyring_path)
        else:
            keyring_path = os.path.join("/", keyring_path)

        if not os.path.isfile(keyring_path):
            self._log.error("Oops: public GPG key not found at: %s", keyring_path)
            sys.exit(1)

        with open(keyring_path, "rb") as keyring:
            gpg_key = keyring.read()

        return gpg_key

    def hash(self):
        """Download and verify the hash for the ISO."""
        hashes = requests.get(self.target.hash_file).content
        if not self.verify_gpg_signature(hashes, self.target.hash_file_signed):
            self._log.error("Oops: GPG signature verification failed")
            sys.exit(1)

        target_hash = ""
        filename = ""
        if self.target.variety == "mini":
            for entry in hashes.decode("utf-8").split("\n"):
                if "mini.iso" in entry:
                    target_hash = entry.split("  ")[0]
                    filename = entry.split("  ")[1].strip("./")
        else:
            for entry in hashes.decode("utf-8").split("\n"):
                # want to pick the latest ISO in the event of multiple releases
                if self.target.variety in entry and self.target.arch in entry:
                    target_hash = entry.split(" ")[0]
                    filename = entry.split(" ")[1].strip("*")

        if not target_hash:
            self._log.error("Oops: No ISO hash found")

        return filename, target_hash

    def download(self):
        """Download the ISO, calculate hash, and and verify it.

        If the expected hash does not match the local hash the
        downloaded ISO will be deleted.
        """
        filename, target_hash = self.hash()
        local_iso = self.download_iso(self.target, filename)

        self._log.debug("Verifying SHA-256")
        self._log.debug(target_hash)
        if target_hash != self.calc_sha256(local_iso):
            self._log.error("Oops: SHA-256 hash mismatch!")
            self.remove_file(local_iso)
            sys.exit(1)

        self._log.debug("Download complete and successfully verified")

    def calc_sha256(self, filename):
        """Calculate SHA256 of a given filename.

        The files can be large so the SHA is calculated in chucks.

        Returns:
            SHA256 digest

        """
        sha256 = hashlib.sha256()
        with open(filename, "rb") as file:
            while True:
                data = file.read(65536)
                if not data:
                    break
                sha256.update(data)

        self._log.debug(sha256.hexdigest())
        return sha256.hexdigest()

    def download_iso(self, iso, filename):
        """Download the ISO with progress bar.

        This uses tqdm to create a progress bar to show the status of
        the download, total time, remaining time, speed, and overall
        percentage done.

        Args:
            iso: ISO URL object

        Returns:
            string, ISO filename

        """
        url = "%s/%s" % (iso.url, filename)
        if self.target.variety == "mini":
            filename = "mini.iso"

        self._log.info("Downloading %s from %s", filename, iso.url)
        response = requests.get(url, stream=True)
        chunk_size = 1024 * 1024

        progress = tqdm(
            total=int(response.headers["Content-Length"]), unit="B", unit_scale=True,
        )

        with open(filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=chunk_size):
                progress.update(len(chunk))
                file.write(chunk)

        progress.close()

        return filename

    def get_ubuntu_release(self, release=None):
        """Return specified Ubuntu release or latest LTS.

        This will return the release that aligns with the given codename
        or release number. If no release is provided, then the latest
        released LTS is returned instead.

        Args:
            release: string, codename or numeric Ubuntu release value
        Returns:
            UbuntuRelease object

        """
        ubuntu = UbuntuReleaseInfo.Data()

        if not release:
            return ubuntu.lts

        if "." in release:
            release = ubuntu.by_release(release)
        else:
            release = ubuntu.by_codename(release)

        if not release.is_supported:
            self._log.error(
                "Oops: '%s' is an unsupported release!" " Please choose from:\n%s",
                release.codename,
                [release.codename for release in ubuntu.supported],
            )
            sys.exit(1)

        return release

    @staticmethod
    def remove_file(filename):
        """Remove the given file.

        Args:
            filename: string, path to file
        """
        try:
            os.remove(filename)
        except OSError:
            pass

    def verify_gpg_signature(self, data, signature_url):
        """Verify GPG signature of a signed file.

        This will setup a new GPG key entry in a temporary directory to
        prevent needing to add the key to the user's keyring. The
        Ubuntu ISO CD singing key will get imported to the keyring.
        Finally, the signed file's signature will be verified with the
        unsigned file.

        The signing key is 0xD94AA3F0EFE21092

        Args:
            data: string, string to verify
            signature_url: string, URL to signature of data

        Return:
            boolean, if verification succeeds

        """
        with tempfile.TemporaryDirectory() as directory_name:
            gpg = gnupg.GPG(gnupghome=directory_name)
            gpg.import_keys(self.ubuntu_cd_public_gpg)

            sig_file = os.path.join(directory_name, "signature.gpg")
            with open(sig_file, "wb") as f:
                f.write(requests.get(signature_url).content)

            return gpg.verify_data(sig_file, data)
