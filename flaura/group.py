# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

from typing import *
import click
class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None,  **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)

    def format_commands(self, ctx, formatter: click.HelpFormatter):
        super().get_usage(ctx)
        formatter.write_paragraph()

        main_commands = list()
        build_commands = list()
        
        for command in super().list_commands(ctx):
                main_commands.append(command)

        with formatter.section("The available commands are"):
            for command in main_commands:
                command: click.Command = super().get_command(ctx, command)
                if command.help:
                    desc = command.help.split("\n")[0]
                else:
                    desc = "No description available"
                formatter.write_text(f"{command.name} - {desc}")
      