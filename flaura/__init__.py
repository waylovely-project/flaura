# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

from flaura.pull import pull
from .home import init
from .upstream import add, list_sources_cmd, remove
import click 
from .merge import merge, merge_cmd
from .group import OrderedGroup 

@click.group(cls=OrderedGroup)
def flaura():
    """Manage upstreams with ease!!
    Flaura is a tool for . It has replacements for Git submodules.
    """
    pass

flaura.add_command(merge_cmd)
flaura.add_command(init)
flaura.add_command(pull)
flaura.add_command(add)
flaura.add_command(remove)

flaura.add_command(list_sources_cmd)
