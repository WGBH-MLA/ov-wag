#!/usr/bin/env python3
from subprocess import run as sub_run
from typing import List, Optional

from loguru import logger as log
from trogon import Trogon
from typer import Argument, Context, Exit, Option, Typer
from typing_extensions import Annotated

# from typer.main import get_group
COMPOSE = "docker compose -f docker-compose.yml"
DEV = "-f dev.yml"
MANAGE = "run --entrypoint python wagtail manage.py"

app = Typer(context_settings={'help_option_names': ['-h', '--help']})


def run(cmd: str):
    sub_run(cmd, shell=True, check=True)


@app.command()
def tui(ctx: Context):
    """Run an interactive TUI"""
    Trogon(app, click_context=ctx).run()


def version_callback(value: bool):
    """Print the version of the program and exit"""
    if value:
        from .ov_wag._version import __version__

        print(f'v{__version__}')

        raise Exit()


@app.command()
def dev(
    args: Annotated[
        Optional[List[str]],
        Option(help='Additional arguments to pass to the build step'),
    ] = []
):
    """Run the dev environment"""
    run(f'{COMPOSE} {DEV} up {" ".join(args)}')


@app.command()
def build(
    args: Annotated[
        Optional[List[str]],
        Option(help='Additional arguments to pass to the build step'),
    ] = [],
):
    """Build the dev environment"""
    run(f'{COMPOSE} build {" ".join(args)}')


@app.command()
def shell():
    """Enter into a python shell inside the dev environment"""
    run(f'{COMPOSE} {DEV} {MANAGE} shell')


@app.command()
def manage(cmd: Annotated[List[str], Argument(help='The manage.py command to run')]):
    """Run a manage.py function"""
    run(f'{COMPOSE} {DEV} {MANAGE} {" ".join(cmd)}')


@app.command('cmd')
def cmd(
    cmd: Annotated[List[str], Argument(help='The command to run')],
    entrypoint: Annotated[
        str, Option('--entrypoint', '-e', help='The entrypoint to use')
    ] = 'bash',
):
    """Run a manage.py function"""
    run(f'{COMPOSE} {DEV} run -it --entrypoint $ENTRYPOINT wagtail {" ".join(cmd)}')


@app.callback()
def main(
    ctx: Context,
    version: bool = Option(
        None,
        '--version',
        '-V',
        callback=version_callback,
        is_eager=True,
        help='Show the version and exit.',
    ),
    verbose: bool = Option(None, '--verbose', '-v', help='Show verbose output.'),
):
    if not verbose:
        log.remove()
