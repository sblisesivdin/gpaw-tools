---
layout: default
nav_order: 4
title: Development
has_children: true
permalink: /development
---

# Development

## Information

* [Input File Keywords](inputfilekeywords.md)
* [Release Notes](releasenotes.md)

## Contributing

We welcome contributions and hope this guide will make the `gpaw-tools` code repository easier to understand. It is important to mention that the `gpaw-tools` software development is run voluntarily and therefore we need to build a community that can support user questions, attract new users, maintain documentation, write tutorials, and develops new features to make this software a useful tool for all users.

### Being Respectful

Please show empathy and kindness towards other people, other software, and communities that work diligently to develop other tools.

In pull requests and issues, please do not speak in a way that negatively portrays other people or their work.

### Cloning the Source Repository

Before cloning the source repository to your computer, please visit the [installation page](https://sblisesivdin.github.io/gpaw-tools/installation/) of `gpaw-tools` to install ASE, GPAW, and other all needed packages to your computer. Then, you can clone the source of the `gpaw-tools` from related repository:
[Main Github repository](https://github.com/sblisesivdin/gpaw-tools) by:

    git clone https://github.com/sblisesivdin/gpaw-tools.git
    cd gpaw-tools

### Questions

We do not have any email-list, IRC channel, Slack room, etc. 
* For general questions about the project, and all other things, we will use the [Discussions](https://github.com/sblisesivdin/gpaw-tools/discussions) page of the GitHub repository. 
* For more technical problems, you are welcome to create an issue on the [Issues](https://github.com/sblisesivdin/gpaw-tools/issues) page of the GitHub repository. Posting to the issues page allows community members with the required expertise to answer your question, and the information obtained remains available to other users on the issues page for future usage.

### Reporting Bugs and Feature Requests


If you encounter any bugs, crashes, or quirks while using the code, please report it on the [Issues](https://github.com/sblisesivdin/gpaw-tools/issues) page with an appropriate tag so that the developers can take care of it immediately. When reporting an issue, please be overly descriptive so we can reproduce it. If possible, provide trackbacks, screenshots, and sample files to help us resolve the issue. For reporting a bug, please create an issue with the "Bug report" template.

Please do not hesitate to submit ideas for improvements to the `gpaw-tools` software. To suggest an improvement, please create an [Issue](https://github.com/sblisesivdin/gpaw-tools/issues) with the "Feature Request" template. Please use descriptive and extensive information (links, videos, possible screenshots, etc.) to help the developers implement this functionality.

### Contributing New Code

If you have an idea to solve a bug or implement a new feature, please first create an issue as a bug report/feature request and we can use that issue as a discussion thread to resolve the implementation of the contribution.

### Licensing

All code is licensed under the MIT License. If you didn't write the code yourself, it's your responsibility to make sure the existing license is compatible and included with the contributed files.

### New Release

In each new release, the following steps must be completed.
- Update __version__ variable in `gpawsolve.py` (Approximate place is line 168) as vYY.m.x. Here YY is year and m (or mm) is month, and x is the step number of release for that month. There is no minor or major release.
- Update __version__ variable in `asapsolve.py` (Approximate place is line 77) as vYY.m.x. Here YY is year and m (or mm) is month, and x is the step number of release for that month. There is no minor or major release.
- Click `Draft a new release`on releases page and create a new tag with the version number.
- Give a general title, give some highlights information, write Release Notes (copy/paste from gh-pages/releasenotes.md webpage).
- Select `Create a discussion for this release` and then finish release.
- Update __version__ variable in `gpawsolve.py` and `asapsolve.py` as vYY.m.y. Here y= (x+1)b1. For example for x=0 -> y=1b1 for x=1 -> y=2b1 ...etc...
- Update `gh-pages/releasenotes.md`
- Update `gh-pages/index.md`


