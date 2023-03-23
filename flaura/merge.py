# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

from collections import namedtuple
import hashlib
import shutil 
from pathlib import Path
import tomlkit
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
@click.option("--only")
def merge_cmd(origin, current_path, home, ours, theirs, union, only): 
    """Merge a URI source with a folder. At the moment only supports file:// URI.
    Uses the GNU RCS' merge command if available, but will use Git's merge-file command if Git is installed!!

    If there is a conflict, Git merge conflicts will appear in the files, and you can use Git integrations in your code editors to resolve them! 
    Pretty much this command runs like Git's behavior!

    origin: "The URI source to merge into current_path. At the moment. Example: file://../smithay/anvil"
    """
    merge(origin, current_path, home, ours, theirs, union, only)
    
def merge(origin, current_path: Path, home, ours, theirs, union, only):
    url = urlparse(origin)

    if url.scheme == "file":
        path = Path(url.netloc+"/"+url.path)
        if not dist.exists():
            click.echo(f"{str(dist)} does not exist!", err=True)
            exit(1)
        merge_inner(path, current_path, home=home, ours=ours, theirs=theirs, union=union)
    if url.scheme.startswith("git+") or url.netloc == "github.com":
        url2 = ParseResult(url.scheme.removeprefix("git+"), url.netloc, url.path, url.params, url.query, "")
        dist = get_home().parent.joinpath(".flaura", "origins", 
        (url.scheme + "+" + url.netloc+"+"+url.path.split("/")[-2] + "/" +url.path.split("/")[-1] + "+" +  hashlib.md5(urlunparse(url2).encode("utf-8")).hexdigest() ) )
        if type(only) == tomlkit.items.String:
            only = str(only)
        if not dist.exists() or len(list(dist.iterdir())):
            if not dist.exists():
                dist.mkdir(parents=True)
            if only:
                only_a = []
                if type(only) is str:
                    only_a = [only]
                elif type(only) is list:
                    only_a = only
                subprocess.check_output(["git", "init"], cwd=dist)
                subprocess.check_output(["git", "sparse-checkout", "set"], cwd=dist)
                with open(dist.joinpath(".git/info/sparse-checkout"), 'w') as file:
                    file.write("\n".join(only_a))
                output = subprocess.run(["git", "remote", "set-url", "origin", urlunparse(url2)],  stderr=subprocess.PIPE, encoding="utf-8", cwd=dist)
                if output.stderr:
                    if output.stderr == "error: No such remote 'origin'":
                        subprocess.check_output(["git", "remote", "add", "origin", urlunparse(url2)], cwd=dist)
                    else:
                        print(output.stderr)
                        exit(1)
                
               
                subprocess.check_output(["git", "pull", "origin", url.fragment])
          


            else:
                command =   ["git", "clone", urlunparse(url2), dist]
                if url.fragment:
                  command.extend(["-b", url2.fragment])
                subprocess.check_output(command, cwd=dist)
        else: 
            branch = url2.fragment or subprocess.check_output(["git", "remote", "set-head", "origin", "-a"]).removeprefix("origin/HEAD set to ")


            subprocess.check_output(["git", "switch", f"origin/{branch}"], cwd=dist)
       
        end_dist = dist
        if type(only) == str:
            end_dist = dist.joinpath(only)
        
        if end_dist.exists():
            merge_inner(end_dist, current_path, home=home, ours=ours, theirs=theirs, union=union)
        else: 
            print(f"{end_dist} does not exist. so we can't merge it")
            exit(1)
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
                            
                        subprocess.check_output([*command, target, path, target, 
                       ], check=True)
            else:
                shutil.copyfile(path, target)
        