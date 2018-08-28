# Ubuntu ISO

[![Build Status](https://travis-ci.org/powersj/ubuntu-iso.svg?branch=master)](https://travis-ci.org/powersj/ubuntu-iso) [![Snap Status](https://build.snapcraft.io/badge/powersj/ubuntu-iso.svg)](https://build.snapcraft.io/user/powersj/ubuntu-iso)

Download the latest Ubuntu ISOs

## Install

Users can obtain ubuntu-iso as a snap:

```shell
snap install ubuntu-iso
```

Or via PyPI:

```shell
pip3 install ubuntu-iso
```

## Usage

At the very least a user needs to provide the Ubuntu release's codename and flavor to download:

```shell
ubuntu-iso bionic desktop
```

Other options available to a user:

* `--arch` to specify a different architecture (default: amd64)
* `--daily` to download the daily development ISO
* `--dry-run` to not download anything and instead show the URL that would be downloaded
* `--debug` provides additional verbose output

```shell
ubuntu-iso <release> <platform> [--arch <arch>] [--daily] [--dry-run] [--debug]
```
