# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

import click 
from pathlib import Path 
import os
from typing import Optional 
def _get_home_from_cwd(parent: Optional[Path]):
    cwd = parent or Path.cwd()
    home = cwd.joinpath("flaura.toml")
    if home.exists():
        return home
    else:
        if cwd.parent == Path.home() or cwd.parent == cwd.root:
            click.echo("We couldn't find any flaura.toml file!! Please initiate them first by adding an upstream!!! See flaura upstream -h", err=True)
            exit(1)
        _get_home_from_cwd(cwd.parent)
def get_home():
    return Path(os.environ.get("FLAURA_HOME") or _get_home_from_cwd(None))


@click.command()
def init():
    """Initialize a flaura upstreams file in the current working directory!!"""
    Path.cwd().joinpath("flaura.toml").touch()