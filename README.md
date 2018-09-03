# Ubuntu ISO Download

[![Build Status](https://travis-ci.org/powersj/ubuntu-iso-download.svg?branch=master)](https://travis-ci.org/powersj/ubuntu-iso-download) [![Snap Status](https://build.snapcraft.io/badge/powersj/ubuntu-iso-download.svg)](https://build.snapcraft.io/user/powersj/ubuntu-iso-download)

Download the latest Ubuntu ISOs

This is used to download Ubuntu ISOs and verify the download. The SHA256 hash of the ISO is downloaded and the signed GPG file used to verify that the file is valid. Once downloaded, the hash of the ISO is compared to the expected value and either confirmed or the file is deleted.

## Install

Users can obtain ubuntu-iso-download as a snap:

```shell
snap install ubuntu-iso-download --classic
```

Or via PyPI:

```shell
pip3 install ubuntu-iso-download
```

## Usage

A user needs to provide at the very last the flavor of ISo to download. By default, this will then download the latest released LTS of that flavor:

```shell
# Latest LTS of Ubuntu desktop
ubuntu-iso-download desktop
```

A specific, supported release can be specified as well:

```shell
# Ubuntu Xenial of Ubuntu server
ubuntu-iso-download server xenial
# Ubuntu Cosmic of Xubuntu
ubuntu-iso-download xubuntu cosmic
```

Other options available to a user:

* `--dry-run` to not download anything and instead show the URL that would be downloaded
* `--debug` provides additional verbose output

```shell
ubuntu-iso-download <platform> [release] [--dry-run] [--debug]
```
