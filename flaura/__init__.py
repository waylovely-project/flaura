# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

from .merge import merge
import click 
from .group import OrderedGroup 

@click.group(cls=OrderedGroup)
def flaura():
    pass

flaura.add_command(merge)