import subprocess
from setuptools import setup
from pathlib import Path

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

git_commit_epoch = 0

try:
    git_commit_epoch = (
        subprocess.check_output(["git", "show", "-s", "--format=%ct", "HEAD"])
        .strip()
        .decode()
    )
    open("version.txt", "w").write(git_commit_epoch)
except:  # noqa
    git_commit_epoch = open("version.txt").read()

setup(
    name="codetocad",
    version=f"0.4.{git_commit_epoch}",
    description="3D modeling automation in your favorite modeling software.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CodeToCAD/CodeToCAD",
    author="CodeToCAD",
    author_email="shehab@codethatdown.com",
    license="GPL v3",
    entry_points={
        "console_scripts": ["codetocad=codetocad.run:execute_launcher"],
    },
    packages=[
        "codetocad",
        "codetocad.core",
        "codetocad.core.shapes",
        "codetocad.enums",
        "codetocad.interfaces",
        "codetocad.launchers",
        "codetocad.proxy",
        "codetocad.utilities",
        "providers.sample",
    ],
    install_requires=[],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
