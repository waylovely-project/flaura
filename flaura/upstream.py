# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

import click 
from .home import get_home
@click.command()
def upstream():
    get_home()