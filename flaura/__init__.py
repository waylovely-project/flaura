from .merge import merge
import click 
from .group import OrderedGroup 

@click.group(cls=OrderedGroup)
def flaura():
    pass

flaura.add_command(merge)