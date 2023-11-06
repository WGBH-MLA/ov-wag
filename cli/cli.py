from typing import List, Optional

from loguru import logger as log
from trogon import Trogon
from typer import Argument, Context, Option, Typer
from typer.main import get_group
from typing_extensions import Annotated

from .utils import AliasGroup, run, version_callback

COMPOSE = "docker compose -f docker-compose.yml"
DEV = "-f dev.yml"
MANAGE = "run --entrypoint python wagtail manage.py"
TESTS = '-f tests.yml'

app = Typer(cls=AliasGroup, context_settings={'help_option_names': ['-h', '--help']})


@app.command('d | dev')
def dev(
    args: Annotated[
        Optional[List[str]],
        Option(help='Additional arguments to pass to the build step'),
    ] = None
):
    """Run the dev environment"""
    if args is None:
        args = []
    run(f'{COMPOSE} {DEV} up {" ".join(args)}')


@app.command('b | build')
def build(
    args: Annotated[
        Optional[List[str]],
        Option(help='Additional arguments to pass to the build step'),
    ] = None,
):
    """Build the dev environment"""
    run(f'{COMPOSE} build {" ".join(args)}')


@app.command('s | shell')
def shell():
    """Enter into a python shell inside the dev environment"""
    run(f'{COMPOSE} {DEV} {MANAGE} shell')


@app.command('m | manage')
def manage(cmd: Annotated[List[str], Argument(help='The manage.py command to run')]):
    """Run a manage.py function"""
    run(f'{COMPOSE} {DEV} {MANAGE} {" ".join(cmd)}')


@app.command('c | cmd')
def cmd(
    cmd: Annotated[List[str], Argument(help='The command to run')],
    entrypoint: Annotated[
        str, Option('--entrypoint', '-e', help='The entrypoint to use')
    ] = '"bash -c"',
):
    """Run a command inside the dev environment"""
    run(
        f'{COMPOSE} {DEV} run -it --entrypoint {entrypoint} wagtail "{ " ".join(cmd) }"'
    )


@app.command('t | test')
def test():
    """Run the test suite"""
    run(f'{COMPOSE} {TESTS} run wagtail-tests')


@app.command('cover | coverage')
def coverage():
    """Run the test suite with coverage"""
    run(f'{COMPOSE} {TESTS} run --entrypoint coverage wagtail-tests lcov')


@app.command('tui')
def terminal_ui(ctx: Context):
    """Run an interactive TUI"""
    Trogon(get_group(app), click_context=ctx).run()


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
