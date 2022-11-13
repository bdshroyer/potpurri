# potpurri
Useful credential-less things I haven't organized yet but would like to keep under version control.


## Contents

### ds-env-setup

A Bash script for setting up and maintaining new Python environments using my preferred data science packages.
* *Motivation:* Installing and upgrading my preferred packages is simple, but involves some drudge work.
* *Requirements:* This script assumes you have Anaconda 3 installed.
* *Side Effects:* A new Python environment is created in conda, and conda gets updated prior to that creation.
* *Notes:* The package's options are pretty fine-grained due to dependency management complexities (TFX libraries in particular do not appear to place nicely with the Tensorflow MacOS packages used to enable AMD GPUs). If you care about AMD GPUs, you're probably stuck on Python 3.9; otherwise use the newest version for which you can get Tensorflow support on Mac so that you can install the TFX libraries without a bunch of OS-specific dependencies getting in the way).

### vim-package.py

A tool for automating installation and updates of Github-based Vim plugins.
* *Motivation:* I was switching over to the Vim 8 plugin manager, and I figured I'd automate the installation and update of said plugins, since I'm almost never in the `.vim` directory and never think to do it.
* *Requirements:*
  * Python 3
  * Vim 8 (older versions don't have the native plugin manager)
  * the [GitPython client](https://github.com/gitpython-developers/GitPython).
  * The [PyYAML](https://pyyaml.org/wiki/PyYAMLDocumentation) library.
* *Side Effects:* Installs new Vim plugins in a specified plugin directory.
