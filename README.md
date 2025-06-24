![CI](https://github.com/WGBH-MLA/ov-wag/actions/workflows/CI.yml/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/WGBH-MLA/ov-wag/badge.svg)](https://coveralls.io/github/WGBH-MLA/ov-wag)

# Open Vault: Wagtail

#### From GBH

Wagtail CMS for [Open Vault](https://openvault.wgbh.org/)

## Documentation

### [User Documentation](https://wgbh-mla.github.io/ov-wag/)

## Usage

### Install

The published version can be installed using pip:

`pip install ov-wag`

#### Local installation

For local development, install [uv](https://docs.astral.sh/uv/) for dependency management.

`pip install uv`

##### Clone the repo:

`git clone https://github.com/WGBH-MLA/ov-wag.git`

##### Install development dependencies:

```bash
uv sync
```

### Scripts

Common functions can be executed as files in the `scripts/` directory

See `scripts/` for detailed usage on each.

#### Examples

`./scripts/dev` will start the development server locally.

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
    - `ov c bash`
    - `ov c python3 -c "print('OpenVault!')"`

## develop

### pre-commit secret scanning

0. Install [ggshield](https://docs.gitguardian.com/ggshield-docs/getting-started)

```shell
pip install ggshield
# or
brew install gitguardian/tap/ggshield
```

1. Login to gitguardian

```shell
ggshield auth login
```

2. Install the pre-commit hooks

```shell
pre-commit install
```

## Credits

Created by the [Media Library and Archives](https://www.wgbh.org/foundation/archives) at [GBH](https://wgbh.org)
