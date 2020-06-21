# Ubuntu ISO Download

[![Build Status](https://travis-ci.com/powersj/ubuntu-iso-download.svg?branch=master)](https://travis-ci.com/powersj/ubuntu-iso-download) [![Snap Status](https://build.snapcraft.io/badge/powersj/ubuntu-iso-download.svg)](https://build.snapcraft.io/user/powersj/ubuntu-iso-download)

[![Get it from the Snap Store](https://snapcraft.io/static/images/badges/en/snap-store-black.svg)](https://snapcraft.io/ubuntu-iso-download)

Download the latest Ubuntu ISOs

This is used to download Ubuntu ISOs and verify hash of the download. The following flavors are available:

* Ubuntu Desktop
* Ubuntu Server
* Ubuntu Netboot (mini.iso)
* Kubuntu
* Lubuntu
* Ubuntu Budgie
* Ubuntu Kylin
* Ubuntu MATE
* Ubuntu Studio
* Xubuntu

The release is the codename and must be a currently supported release and defaults to the latest LTS. Only the amd64 architecture is supported for download.

For verification, the SHA-256 hash file and signed GPG hash file are both downloaded. The signed GPG file is used to verify that the hash file is valid and the expected hash saved. Once the ISO is downloaded, the SHA-256 hash is calculated and compared to the expected value. If a mismatch occurs the download ISO is deleted.

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
# Latest LTS of Ubuntu desktop and server
ubuntu-iso-download desktop
ubuntu-iso-download server
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
