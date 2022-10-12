# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

from pathlib import Path
import click 
from .home import get_home
import tomlkit
@click.group()
def upstream():
    """Commands to manage upstreams!! <3"""
    pass

@click.command()
@click.argument("origin")
@click.argument("path", required=False)
@click.option("--home", is_flag=True)
def add(origin, path, home):
    """Add an upstream! 
    
    """
    home_path = get_home()
    if home:
        path = home_path.parent()
    else: 
        if not path:
            print("Please specify a path!!")
            exit(1)
        path = Path(path)
    with home_path.open(mode="r") as home_fd:
        home = tomlkit.parse(home_fd.read())
        upstream = tomlkit.table()
        upstream["origin"] = origin
        home.append(str(path), upstream)

        with home_path.open(mode="w") as home_fd:
            home_fd.write(tomlkit.dumps(home))
    
upstream.add_command(add)