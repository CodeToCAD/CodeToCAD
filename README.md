<div align="center">
    <a href="https://pypi.org/project/codetocad/0.2.1688153771/">
    <h1>CodeToCAD</h1>
    </a>
    <p><strong>Automate Digital Manufacturing With Your Existing Tools</p>
</div>
<p align="center">
   <!-- <a href="https://codetocad.github.io/CodeToCAD/docs.html"><img src="https://img.shields.io/badge/Read_the_docs-white?logo=readthedocs&logoColor=black"/></a> -->
   <a href="https://discord.gg/MnZEtqwt74"><img alt="Discord" src="https://img.shields.io/discord/955573351806562335?logo=discord&logoColor=black&label=Discord&labelColor=white&color=blue"></a>
   <a href="https://github.com/CodeToCAD/CodeToCAD/stargazers"><img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/CodeToCAD/CodeToCAD"/></a>
   <a href="https://github.com/search?q=repo%3ACodeToCAD%2FCodeToCAD++language%3APython&type=code"><img alt="GitHub top language" src="https://img.shields.io/github/languages/top/CodeToCAD/CodeToCAD?logo=python&labelColor=white&color=blue"></a>
   <!-- <a href="https://codetocad.github.io/CodeToCAD/examples.html"><img alt="Static Badge" src="https://img.shields.io/badge/Examples-white?logo=internetarchive&logoColor=black"></a> -->
</p>

**Maintainers Note**: This month (August 2025) we're focused on implementing the new API discussed in [New API](./devlog/2-new-api.ipynb). This new API migrates old features and improves the overall low-level sketching and querying features. Thanks for your patience while we bring these changes out! (Updated July 28, 2025)

## Table of Contents

- [What is CodeToCAD](#what-is-codetocad)
- [Why CodeToCAD?](#why-codetocad)
- [Maintainer Notes Archive](./maintainer-notes.md)
- [Developer Logs](#dev-logs)
- [Additional Resources](#additional-resources)
- [Contributors](#contributors)
- [FAQ](#faq)

## Getting Started

Follow the [0-getting-started.ipynb](./devlog/0-getting-started.ipynb) notebook to install dependencies and run CodeToCAD.

## What is CodeToCAD
CodeToCAD is an open source digital manufacturing automation. Its goal is to allow engineers and developers to write python scripts that can be checked into source control, collaborated on, and run on any supported CAD, modeling, simulation, FEA or machining software. It's a one-stop-shop for designing hardware, electrical, software, and getting it ready for manufacturing.

## Why CodeToCAD?

✅ Simplified modeling interface - it's all text! No more scrolling and clicking into sub-menus to edit your models.

🔓 Not vendor locked - your models are created in an open-source language. If you want to use another software, you do not lose the features you have defined. Note: There is no guarantee that a model created for, e.g. Blender, will work right away for another software, but with some refactoring, it theoretically should!

🪶 Lightweight and portable. All you need is a text-editor to model. You can occasionally fire-up your modeling software to run your creations.

💪 Leverages existing programming languages, like Python. You can keep using the languages you're familiar with and love. There is no one-off language you and your team has to learn. Use CodeToCAD like a library or a framework.

🚦Easy version control. Your models are written in code, you can use industry-loved git to keep track of versions of your models.

💕 Built by people who believe in automation and that modeling workflows should be intuitive, reliable and most importantly free and open source!

<div align="center">
<image src="https://raw.githubusercontent.com/CodeToCAD/CodeToCAD/codetocad_legacy/docs/images/three_axis_mill.gif"/>
</div>

## Dev Logs

0. [Getting Started](./devlog/0-getting-started.ipynb)
1. [Topology](./devlog/1-topology.ipynb)
2. [New Api](./devlog/2-new-api.ipynb)
3. [Blender Adapter](./devlog/3-blender-adapter.ipynb)

## Additional Resources
 - [CodeToCAD docs](https://codetocad.github.io/CodeToCAD/docs.html)
 - [CodeToCAD PyPI](https://pypi.org/project/codetocad/)

## Contributors
Thank you to all our contributors for their invaluable time, effort, and expertise in making CodeToCAD possible: 

<a href="https://github.com/CodeToCAD/CodeToCAD/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=CodeToCAD/CodeToCAD" />
</a>


## FAQ

1. Why Blender? Isn't this an engineering tool?

When this project started, Blender offered a very mature API for development. You can run CodeToCAD scripts in Onshape and Fusion360. The only limitation is how many CodeToCAD features have been implemented for the software you are trying to use. We provide [documentation](https://codetocad.github.io/CodeToCAD/docs.html) to allow you to filter supported features.

> Side-note: Blender not being "accurate" for engineering tasks is a misunderstanding. You can generate shapes that are just as precise as CAD software in Blender - as long as there are no splines, fillets or curved surfaces. Blender thrives on mesh geometry. A bevel in Blender will consist of hundreds of vertices. The discrete nature of this geometry makes it susceptible to tessellations, which can be smoothed out by increasing the resolution of the splines. This in turn increases the number of vertices, edges, and faces, and you soon run out of RAM to process intricate models. At the time of writing, to our knowledge, NURBs geometry in Blender cannot be exported out of the software. At least without addons.

