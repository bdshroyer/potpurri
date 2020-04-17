# potpurri
Useful credential-less things I haven't organized yet but would like to keep under version control.


## Contents

### ds-env-setup

A Bash script for setting up and maintaining new Python environments using my preferred data science packages.
* *Motivation:* Installing and upgrading my preferred packages is simple, but involves some drudge work.
* *Requirements:* This script assumes you have Anaconda 3 installed.
* *Side Effects:* A new Python environment is created in conda, and conda gets updated prior to that creation.

### vim-package.py

A tool for automating installation and updates of Github-based Vim plugins.
* *Motivation:* I was switching over to the Vim 8 plugin manager, and I figured I'd automate the installation and update of said plugins, since I'm almost never in the `.vim` directory and never think to do it.
* *Requirements:* Python 3, Vim 8 (older versions don't have the native plugin manager), the [GitPython client](https://github.com/gitpython-developers/GitPython).
* *Side Effects:* Installs new Vim plugins in a specified plugin directory.
