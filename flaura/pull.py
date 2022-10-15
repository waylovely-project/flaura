import click 
from urllib.parse import urlparse
from .home import get_home
from .merge import merge
import tomlkit

@click.command()
@click.option("--ours", is_flag=True)
@click.option("--theirs", is_flag=True)
@click.option("--union", is_flag=True)
def pull(ours, theirs, union):
    home_path = get_home()
    
    with home_path.open(mode="r") as home_fd:
        home = tomlkit.parse(home_fd.read())
        for upstream in home.keys():
            if "origin" not in home[upstream]:
                click.echo(f"{upstream}", err=True)
                exit(1)
            dist = home_path.parent.joinpath(home[upstream].get("folder") or upstream)
            if not dist.exists():
                click.echo(f"{str(dist)} does not exist!", err=True)
                exit(1)
            merge(home[upstream]["origin"], dist, False, ours, theirs, union)
            