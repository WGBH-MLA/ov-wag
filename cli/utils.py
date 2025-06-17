from re import split
from subprocess import run as sub_run

from ov_wag._version import __version__
from typer import Exit
from typer.core import TyperGroup


def run(cmd: str):
    sub_run(cmd, shell=True, check=True)


def version_callback(value: bool):
    """Print the version of the program and exit"""
    if value:

        print(f'v{__version__}')

        raise Exit()


class AliasGroup(TyperGroup):
    """Create an alias for a command.

    Blatenly stolen from: https://github.com/tiangolo/typer/issues/132#issuecomment-1714516903
    """

    _CMD_SPLIT_P = r'[,| ?\/]'

    def get_command(self, ctx, cmd_name):
        cmd_name = self._group_cmd_name(cmd_name)
        return super().get_command(ctx, cmd_name)

    def _group_cmd_name(self, default_name):
        for cmd in self.commands.values():
            if cmd.name and default_name in split(self._CMD_SPLIT_P, cmd.name):
                return cmd.name
        return default_name
