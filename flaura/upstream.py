import click 
from .home import get_home
@click.command()
def upstream():
    get_home()