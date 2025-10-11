"""
insert_function.py

Usage:
    python insert_function.py --target path/to/file.py --snippet path/to/snippet.py [--marker "MARKER"] [--append] [--backup]
Options:
    --target   Path to the python file to modify.
    --snippet  Path to a file that contains the function(s) to insert (plain text).
    --marker   A unique line (string) where the snippet will be inserted after. If omitted, requires --append.
    --append   If marker not provided, append snippet to the end of file.
    --backup   Create a backup copy target.bak before modifying.
    --git-commit "message"  Optional: if provided, will run git add/commit with that message (requires git and being inside a git repo).
    --git-branch BRANCH_NAME  Optional: switch/create this branch before committing. Only used if --git-commit is supplied.
"""
import argparse
import shutil
import subprocess
from pathlib import Path
from typing import Optional
import sys

def read_file(path: Path):
    return path.read_text(encoding='utf-8')

def write_file(path: Path, text: str):
    path.write_text(text, encoding='utf-8')

def make_backup(path: Path):
    bak = path.with_suffix(path.suffix + '.bak')
    shutil.copy2(path, bak)
    return bak

def insert_snippet(target: Path, snippet: Path, marker: Optional[str] = None, append: bool = False, backup: bool = True):
    if not target.exists():
        raise FileNotFoundError(f"target file not found: {target}")
    if not snippet.exists():
        raise FileNotFoundError(f"snippet file not found: {snippet}")

    if backup:
        bak = make_backup(target)
        print(f"Backup created: {bak}")

    target_text = read_file(target)
    snippet_text = read_file(snippet).rstrip() + '\n\n'  # ensure trailing newline

    if marker:
        if marker not in target_text:
            raise ValueError(f"Marker not found in target file: {marker!r}")
        # insert after the marker line
        parts = target_text.split(marker, 1)
        new_text = parts[0] + marker + '\n' + snippet_text + parts[1]
        print(f"Inserted snippet after marker: {marker!r}")
    else:
        if not append:
            raise ValueError("No marker provided and --append not set.")
        new_text = target_text.rstrip() + '\n\n' + snippet_text
        print("Appended snippet to end of file.")

    write_file(target, new_text)
    print(f"Updated file written: {target}")

def git_switch_branch(branch_name: str):
    # create branch if it doesn't exist and switch
    subprocess.check_call(['git', 'checkout', '-B', branch_name])

def git_commit_and_push(target: Path, message: str, branch_name: Optional[str] = None):
    if branch_name:
        git_switch_branch(branch_name)
        print(f"Switched/created branch: {branch_name}")

    subprocess.check_call(['git', 'add', str(target)])
    subprocess.check_call(['git', 'commit', '-m', message])
    # do not auto-push without user's confirmation in some environments — but we will push by default
    subprocess.check_call(['git', 'push', '--set-upstream', 'origin', branch_name] if branch_name else ['git', 'push'])
    print("Changes committed and pushed.")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', required=True)
    ap.add_argument('--snippet', required=True)
    ap.add_argument('--marker', required=False)
    ap.add_argument('--append', action='store_true')
    ap.add_argument('--backup', action='store_true')
    ap.add_argument('--git-commit', required=False, help='Commit message to use (optional). If provided, will git add/commit and push.')
    ap.add_argument('--git-branch', required=False, help='Branch name to create/switch to before committing (optional).')
    args = ap.parse_args()

    target = Path(args.target)
    snippet = Path(args.snippet)

    try:
        insert_snippet(target, snippet, marker=args.marker, append=args.append, backup=args.backup)
    except Exception as e:
        print("ERROR:", str(e))
        sys.exit(1)

    if args.git_commit:
        try:
            git_commit_and_push(target, args.git_commit, args.git_branch)
        except subprocess.CalledProcessError as e:
            print("Git command failed:", e)
            sys.exit(2)

if __name__ == '__main__':
    main()