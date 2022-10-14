# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

from pathlib import Path
import click 
from .home import get_home
import tomlkit
from os import path

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
    
@click.command()
@click.argument("name", type=str)
def remove(name):
    home_path = get_home()
    
    with home_path.open(mode="r") as home_fd:
        home = tomlkit.parse(home_fd.read())
        home.remove(name)
        with home_path.open(mode="w") as home_fd:
            home_fd.write(tomlkit.dumps(home))



@click.command("list")
def list_sources_cmd():
     list_sources()

def list_sources():
    home_path = get_home()
    with home_path.open(mode="r") as home_fd:
        home = tomlkit.parse(home_fd.read())
        for upstream in home.keys():
            click.secho(" " + upstream + " ", bg="green", fg="bright_white")
            click.echo(click.style("url: ", bold=True) + home[upstream]["origin"])
            click.echo(click.style("folder: ", bold=True) + (home[upstream].get("folder") or str(home_path.parent.joinpath(upstream))) + "\n")
            
