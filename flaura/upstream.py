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
    
    The origin 
    """
    home_path = get_home()

    home = home_path.open(mode="rw")

    home.read()

upstream.add_command(add)