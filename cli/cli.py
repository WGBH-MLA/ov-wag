from typing import List, Optional

from loguru import logger as log
from trogon import Trogon, tui
from typer import Argument, Context, Exit, Option, Typer
from typer.main import get_group
from typing_extensions import Annotated

from .utils import AliasGroup, run, version_callback

# from typer.main import get_group
COMPOSE = "docker compose -f docker-compose.yml"
DEV = "-f dev.yml"
MANAGE = "run --entrypoint python wagtail manage.py"

app = Typer(cls=AliasGroup, context_settings={'help_option_names': ['-h', '--help']})


@app.command('t | tui')
def terminal_ui(ctx: Context):
    """Run an interactive TUI"""
    Trogon(get_group(app), click_context=ctx).run()


@app.command('d | dev')
def dev(
    args: Annotated[
        Optional[List[str]],
        Option(help='Additional arguments to pass to the build step'),
    ] = []
):
    """Run the dev environment"""
    run(f'{COMPOSE} {DEV} up {" ".join(args)}')


@app.command('b | build')
def build(
    args: Annotated[
        Optional[List[str]],
        Option(help='Additional arguments to pass to the build step'),
    ] = [],
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
    run(f'{COMPOSE} {DEV} run -it --entrypoint {entrypoint} wagtail "{" ".join(cmd)}"')


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
