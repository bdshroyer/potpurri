## Installs and refreshes vim plugin. At the moment it only works with packages on Github.
## Note that this is not super-robust. It only works for github repos and only for YAML files.

import yaml
import os
import git.exc   # gitpython exceptions.

from argparse import ArgumentParser
from git import Repo


# Assemble argument parser
parser = ArgumentParser(description='Manage VIM packages using vim 8 native package manager')
parser.add_argument("-f", "--file", type=str, help="config file location")
parser.add_argument("-i", "--install-only", help="fetch missing packages without refreshing existing ones.", action="store_true")
parser.add_argument("-u", "--update-only",help="update existing packages without fetching new ones.", action="store_true")
args = vars(parser.parse_args())

# Sanity-check. If both are set it's essentially a no-op, which I'd rather not be surprised by.
if args['install_only'] and args['update_only']:
    print("ERROR: '--install-only' and '--update-only' flags are mutually exclusive.")
    print("Bailing out.")
    exit(1)

# Read in yaml file.
args['file'] = args['file'] or os.path.join(os.getenv('HOME'), '.vim', 'pkg-config.yml')

with open(args['file'], 'r') as f:
    try:
        config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        print(e)


config['package_root'] = config['package_root'] or os.path.join(os.getenv('HOME'), '.vim', 'pack', 'default', 'start')

for package_url in config['packages']:
    package_name = package_url.split('/')[-1]
    package_dir = os.path.join(config['package_root'], package_name)
    try:
        repo = Repo(package_dir)

        if not args['install_only']:
            print("Refreshing package '{}'...".format(package_name))
            repo.remotes.origin.pull()
            print("{} updated.".format(package_name))
        else:
            print("Install-only mode. Skipping {}.".format(package_name))

    except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError) as e:
        print(e)
        if not args['update_only']:
            print("Repo not found. Cloning repo...")
            Repo.clone_from(package_url, package_dir)
            print("{} installed.".format(package_name))
        else:
            print("Update-only mode. Skipping {}.".format(package_name))


print("\nPackage update done.")
