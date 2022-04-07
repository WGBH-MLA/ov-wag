# ov_wag

Experimental - Open Vault Exhibits on Wagtail CMS

## Usage

### Initial setup

Create an empty database file.

```bash
touch db.sqlite3
```

## Init script

Several common functions can be executed with the `ov` init script (using Docker)

For example, `./ov dev` will start the development server locally.

_Note_ For most commands, additional args will be passed on to the parent command.

- `dev` or `d`
  - starts a local development server
- `build` or `b`
  - build (or rebuild) the docker image
- `shell` or `s`
  - starts a shell with all django variables loaded
- `manage` or `m`
  - run a `manage.py` command
- `cmd` or `c`
  - run a command directly on the container
  - e.g.
    - `./ov c bash`
    - `./ov c python3 -c "print('OpenVault')"`
