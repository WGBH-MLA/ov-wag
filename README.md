# ov-wag

![CI](https://github.com/WGBH-MLA/ov-wag/actions/workflows/ci.yml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/WGBH-MLA/ov-wag/badge.svg)](https://coveralls.io/github/WGBH-MLA/ov-wag)

Experimental - Open Vault Exhibits on Wagtail CMS

## Usage

### Init script

Several common functions can be executed with the `ov` init script (using Docker)

#### For example

`./ov dev` will start the development server locally.

_Note_ For most commands, additional args will be passed on to the parent command.

- `dev` | `d`
  - starts a local development server
- `build` | `b`
  - build (or rebuild) the docker image
- `shell` | `s`
  - starts a shell with all django variables loaded
- `manage` | `m`
  - run a `manage.py` command
- `cmd` | `c`
  - run a command directly on the container
  - e.g.
    - `./ov c bash`
    - `./ov c python3 -c "print('OpenVault!')"`
