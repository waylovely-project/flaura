import click 
from urllib.parse import urlparse
from .home import get_home
from .merge import merge


@click.command()
@click.option("--ours", is_flag=True)
@click.option("--theirs", is_flag=True)
@click.option("--union", is_flag=True)
def pull(ours, theirs, union):
    """Pull sources and merge them into their respective place, at least, it attempts to. This is quite buggy. Please report any issues to the GitHub repository :3
    
    This is just a handy frontend to `flaura merge`, but this reads from the flaura.toml configuration file rather than from the arguments and options passed."""
    home_path = get_home()
    
    with home_path.open(mode="r") as home_fd:
        home = tomlkit.parse(home_fd.read())
        for upstream in home.keys():
            if "origin" not in home[upstream]:
                click.echo(f"{upstream}", err=True)
                exit(1)
            dist = home_path.parent.joinpath(home[upstream].get("folder") or upstream)
          
            merge(home[upstream]["origin"], dist, False, ours, theirs, union, home[upstream].get("only"))
            