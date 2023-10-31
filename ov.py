from subprocess import run as sub_run

from loguru import logger as log
from typer import Argument, Context, Exit, Option, Typer
from typing_extensions import Annotated

# from typer.main import get_group
COMPOSE = "docker compose -f docker-compose.yml"
DEV = "-f dev.yml"
MANAGE = "run --entrypoint python wagtail manage.py"

app = Typer(context_settings={'help_option_names': ['-h', '--help']})

try:
    from trogon import Trogon

    @app.command()
    def tui(ctx: Context):
        Trogon(app, click_context=ctx).run()

except ImportError:
    pass


def version_callback(value: bool):
    """Print the version of the program and exit."""
    if value:
        from .ov_wag._version import __version__

        print(f'v{__version__}')

        raise Exit()


@app.command()
def dev():
    sub_run(f'{COMPOSE} {DEV} up', shell=True)


@app.command()
def build():
    sub_run(f'{COMPOSE} build', shell=True)


@app.command()
def shell():
    sub_run(f'{COMPOSE} {DEV} {MANAGE}', shell=True)


@app.command()
def manage(args: Annotated[str, Argument(help='The manage.py command to run')]):
    """Run a manage.py function"""
    print(args)
    sub_run(f'{COMPOSE} {DEV} {MANAGE} {args.join(" ")}', shell=True)


@app.command()
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


if __name__ == "__main__":
    app()
