# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

from collections import namedtuple
import hashlib
import shutil 
from pathlib import Path
import subprocess
from urllib.parse import ParseResult, urlparse, urlunparse
from .home import get_home
import click 
import filecmp
@click.command("merge")
@click.argument("origin", required=False)
@click.argument("current_path", type=Path, required=False)
@click.option("--home", is_flag=True)
@click.option("--ours", is_flag=True)
@click.option("--theirs", is_flag=True)
@click.option("--union", is_flag=True)
def merge_cmd(origin, current_path, home, ours, theirs, union): 
    """Merge a URI source with a folder. At the moment only supports file:// URI.
    Uses the GNU RCS' merge command if available, but will use Git's merge-file command if Git is installed!!

    If there is a conflict, Git merge conflicts will appear in the files, and you can use Git integrations in your code editors to resolve them! 
    Pretty much this command runs like Git's behavior!

    origin: "The URI source to merge into current_path. At the moment. Example: file://../smithay/anvil"
    """
    merge(origin, current_path, home, ours, theirs, union)
    
def merge(origin, current_path: Path, home, ours, theirs, union):
    url = urlparse(origin)

    if url.scheme == "file":
        path = Path(url.netloc+"/"+url.path)

        merge_inner(path, current_path, home=home, ours=ours, theirs=theirs, union=union)
    if url.scheme.startswith("git+") or url.netloc == "github.com":
        url2 = ParseResult(url.scheme.removeprefix("git+"), url.netloc, url.path, url.params, url.query, url.fragment)
        dist = get_home().parent.joinpath(".flaura", "origins", 
        (url.scheme + "+" + url.netloc+"+"+url.path.split("/")[-2] + "/" +url.path.split("/")[-1] + "+" +  hashlib.md5(origin.encode("utf-8")).hexdigest() ) )
        if not dist.exists():
            print(dist)
            dist.mkdir(parents=True)
            subprocess.run(["git", "clone", urlunparse(url2), dist], cwd=dist)

        merge_inner(dist, current_path, home=home, ours=ours, theirs=theirs, union=union)

    else:
        click.echo(f"{url.scheme} for {origin} is not yet implemented. Sorry!! <3", err=True)
        exit(1)
    
        
        

def merge_inner(parent: Path, target_path: Path, **kwargs):
    if not target_path.exists():
        target_path.mkdir(parents=True)
    for path in parent.iterdir():
        target = target_path.joinpath(path.name)
        if path.is_dir():
           merge_inner(path, target) 
        else:
            if target.exists():
                if not filecmp.cmp(path, target):
                    try:
                        path.read_text()

                        suceed = True
                    except UnicodeDecodeError:
                        shutil.move(target, target.with_suffix(".older"))
                        shutil.copy(path, target)
                    
                    if suceed:
                        
                        if shutil.which("merge"):
                            command = ["merge"]
                        elif shutil.which("git"):
                            command = ["git", "merge-file"]
                        options = []

                        if kwargs.get("ours"):
                            options.push( "--ours" )
                        elif kwargs.get("theirs"):
                            options.push( "--theirs" ) 
                        elif kwargs.get("diff3"):
                            options.push( "--diff3" ) 
                        elif kwargs.get("zdiff3"):
                            options.push( "--zdiff3" )
                        elif kwargs.get("union"):
                            options.push( "--union" )
                            
                        subprocess.run([*command, target, path, target, 
                       ], check=True)
            else:
                shutil.copyfile(path, target)
        