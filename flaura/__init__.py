# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

from .home import init
from .merge import merge
from .upstream import upstream
import click 
from .group import OrderedGroup 

@click.group(cls=OrderedGroup)
def flaura():
    """Manage upstreams with ease!!
    Flaura is a tool for . It has replacements for Git submodules.
    """
    pass

flaura.add_command(upstream)
flaura.add_command(merge)
flaura.add_command(init)