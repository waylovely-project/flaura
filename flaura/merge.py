# SPDX-FileCopyrightText: 2022 Fiana Fortressia
#
# SPDX-License-Identifier: MIT OR APACHE-2.0

import shutil 
from pathlib import Path
import subprocess
from urllib.parse import urlparse
import click 
import filecmp
@click.command()
@click.argument("origin", required=False)
@click.argument("current_path", type=Path, required=False)
@click.option("--home", is_flag=True)
@click.option("--ours", is_flag=True)
@click.option("--theirs", is_flag=True)
@click.option("--union", is_flag=True)
def merge(origin, current_path, home, ours, theirs, union): 
    """Merge a URI source with a folder. At the moment only supports file:// URI.
    Uses the GNU RCS' merge command if available, but will use Git's merge-file command if Git is installed!!

    If there is a conflict, Git merge conflicts will appear in the files, and you can use Git integrations in your code editors to resolve them! 
    Pretty much this command runs like Git's behavior!

    origin: "The URI source to merge into current_path. At the moment. Example: file://../smithay/anvil"
    """
    url = urlparse(origin)

    if url.scheme == "file":
        path = Path(url.netloc+"/"+url.path)

        merge_inner(path, current_path, home=home, ours=ours, theirs=theirs, union=union)
        
        

def merge_inner(parent: Path, target_path: Path, **kwargs):
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
                        subprocess.run([*command, target, path, target, 
                        "--ours" if kwargs["ours"] else "", 
                        "--theirs" if kwargs["theirs"] else "", 
                        "--diff3" if kwargs["diff3"] else "", 
                        "--zdiff3" if kwargs["zdiff3"] else "",
                        "--union" if kwargs["union"] else ""])
            else:
                shutil.copyfile(path, target)
        