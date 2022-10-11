import click 
from pathlib import Path 
import os
from typing import Optional 
def _get_home_from_cwd(parent: Optional[Path]):
    cwd = parent or Path.cwd()
    home = cwd.with_name("flaura.toml")
    if home.exists():
        return home
    else:
        if cwd.parent == Path.home() or cwd.parent == cwd.root:
            click.echo("We couldn't find any flaura.toml file!! Please initiate them first by adding an upstream!!! See flaura upstream -h", err=True)
            exit(1)
        _get_home_from_cwd(cwd.parent)
def get_home():
    os.environ.get("FLAURA_HOME") or _get_home_from_cwd(None)