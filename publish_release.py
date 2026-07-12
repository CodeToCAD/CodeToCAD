#!/usr/bin/env python3
"""Tag a CalVer release (YYYY.MM.DD.NN), then `uv build` and `uv publish`.

Version is never stored in pyproject.toml -- setuptools_scm derives it from
the git tag at build time. This script only needs to create+push that tag.
"""

import argparse
import configparser
import datetime
import getpass
import glob
import os
import re
import shutil
import subprocess
import sys

REPO_ROOT = subprocess.run(
    ["git", "rev-parse", "--show-toplevel"],
    cwd=os.path.dirname(os.path.abspath(__file__)),
    check=True,
    capture_output=True,
    text=True,
).stdout.strip()


def run(cmd, **kwargs):
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=REPO_ROOT, check=True, **kwargs)


def capture(cmd):
    return subprocess.run(
        cmd, cwd=REPO_ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()


def confirm(prompt, assume_yes):
    if assume_yes:
        return True
    reply = input(f"{prompt} [y/N] ").strip().lower()
    return reply in ("y", "yes")


def ensure_clean_worktree():
    dirty = subprocess.run(
        ["git", "diff", "--quiet", "HEAD"], cwd=REPO_ROOT
    ).returncode
    if dirty:
        sys.exit(
            "Working tree has uncommitted changes. Commit or stash before releasing."
        )


def next_tag():
    today = datetime.date.today().strftime("%Y.%m.%d")
    existing = capture(
        ["git", "ls-remote", "--tags", "origin", f"v{today}.*"]
    ).splitlines()
    pattern = re.compile(rf"refs/tags/v{re.escape(today)}\.(\d+)$")
    revisions = [int(m.group(1)) for t in existing if (m := pattern.search(t))]
    next_rev = max(revisions, default=0) + 1
    version = f"{today}.{next_rev:02d}"
    return f"v{version}", version


def _read_pypirc_token(path):
    if not os.path.isfile(path):
        return None
    config = configparser.ConfigParser()
    try:
        config.read(path)
        if config.has_section("pypi") and config.has_option("pypi", "password"):
            return config.get("pypi", "password")
    except configparser.Error:
        pass
    # Not valid INI (e.g. a file containing just the raw token) -- use as-is.
    with open(path) as f:
        content = f.read().strip()
    return content or None


def resolve_publish_token(explicit_token):
    if explicit_token:
        return explicit_token
    if os.environ.get("UV_PUBLISH_TOKEN"):
        return os.environ["UV_PUBLISH_TOKEN"]

    for pypirc_path in (
        os.path.join(REPO_ROOT, ".pypirc"),
        os.path.expanduser("~/.pypirc"),
    ):
        token = _read_pypirc_token(pypirc_path)
        if token:
            print(f"Using token from {pypirc_path}")
            return token

    return getpass.getpass("PyPI API token (not saved): ")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-y", "--yes", action="store_true", help="skip confirmation prompts"
    )
    parser.add_argument(
        "--no-publish",
        action="store_true",
        help="tag and build only, skip uv publish",
    )
    parser.add_argument(
        "--token", help="PyPI API token (overrides ~/.pypirc and env var)"
    )
    args = parser.parse_args()

    ensure_clean_worktree()

    branch = capture(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if branch != "main" and not confirm(
        f"Current branch is '{branch}', not 'main'. Continue?", args.yes
    ):
        sys.exit("Aborted.")

    tag, version = next_tag()
    commit = capture(["git", "rev-parse", "--short", "HEAD"])
    print(f"About to tag {commit} ({branch}) as {tag} (package version {version})")
    if not confirm("Create and push this tag?", args.yes):
        sys.exit("Aborted.")

    run(["git", "tag", "-a", tag, "-m", f"Release {tag}"])
    run(["git", "push", "origin", tag])

    shutil.rmtree(os.path.join(REPO_ROOT, "dist"), ignore_errors=True)
    run(["uv", "build"])

    built = sorted(glob.glob(os.path.join(REPO_ROOT, "dist", "*")))
    print("Built:")
    for f in built:
        print(f"  {os.path.basename(f)}")

    if args.no_publish:
        print("Skipping publish (--no-publish).")
        return

    token = resolve_publish_token(args.token)
    env = dict(os.environ, UV_PUBLISH_TOKEN=token)
    run(["uv", "publish"], env=env)

    print(f"Released {tag} (version {version}).")


if __name__ == "__main__":
    main()
