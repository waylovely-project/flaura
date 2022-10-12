# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

import click 
from .home import get_home
@click.group()
def upstream():
    """Commands to manage upstreams!! <3"""
    pass

@click.command()
@click.argument("origin")
@click.argument("path", required=False)
@click.option("--home", is_flag=True)
def add(origin, path):
    """Add an upstream! 
    
    """
    home_path = get_home()

    print("This command is not yet implemented!")
    exit(1)

    with home_path.open(mode="rw") as home_fd:
        home = tomlkit.parse(home_fd.read())

    
upstream.add_command(add)