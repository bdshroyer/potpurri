## Installs and refreshes vim plugin. At the moment it only works with packages on Github.
## Note that this is not super-robust. It only works for github repos and only for YAML files.

import yaml
import os
import git.exc   # gitpython exceptions.

from argparse import ArgumentParser
from git import Repo
from shutil import rmtree


def legacy_packages(config):
    if config.get('packages') is None or config.get('package_root') is None:
        raise KeyError("legacy_packages() error: missing one or more required config fields.")

    keep_packages = set([os.path.basename(pkg) for pkg in config['packages']])
    have_packages = set(os.listdir(config['package_root']))

    return list(have_packages.difference(keep_packages))


def find_repo(package_url: str, package_root: str, update_only: bool = False) -> Repo:
    """
    Attempts to construct a Repo object from the given package directory. If it encounters
    an exception, it will either attempt to clone the repo or simply return None, depending
    on the `update_only` flag.

    Inputs:
        * A string containing the package's URL.
        * A string containing the root path for the package.
        * A boolean flag indicating whether to run in update-only mode..
    Outputs:
        * A Repo object, or None on an exception thrown in update-only mode.
    """
    repo = None

    package_name = package_url.split('/')[-1]
    package_dir = os.path.join(package_root, package_name)

    try:
        repo = Repo(package_dir)

    except (git.exc.NoSuchPathError, git.exc.InvalidGitRepositoryError) as e:
        print(type(e))

        if update_only:
            print("Update-only mode. Skipping {}.".format(package_name))
        else:
            print("Repo not found. Cloning repo...", end='')
            repo = Repo.clone_from(package_url, package_dir)
            print("done.")

    return repo



def main():
    """
    Main control flow of script. Invoked below.
    """

    # Assemble argument parser
    parser = ArgumentParser(description='Manage VIM packages using vim 8 native package manager')
    parser.add_argument("-f", "--file", type=str, help="config file location")
    parser.add_argument("-i", "--install-only", help="fetch missing packages without refreshing existing ones.", action="store_true")
    parser.add_argument("-u", "--update-only",help="update existing packages without fetching new ones.", action="store_true")
    parser.add_argument("-s", "--strict",help="remove any existing repos not listed in the config file.", action="store_true")
    args = vars(parser.parse_args())

    # Sanity-check. If both are set it's essentially a no-op, which I'd rather not be surprised by.
    if args['install_only'] and args['update_only']:
        print("ERROR: '--install-only' and '--update-only' flags are mutually exclusive.")
        print("Bailing out.")
        exit(1)

    # Read in yaml file.
    args['file'] = args.get('file') or os.path.join(os.getenv('HOME'), '.vim', 'pkg-config.yml')

    with open(args['file'], 'r') as f:
        try:
            config = yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)


    config['package_root'] = config.get('package_root') or os.path.join(os.getenv('HOME'), '.vim', 'pack', 'default', 'start')

    # If strict mode is set, then remove any packages not specified in the package configuration file.
    if args['strict']:
        for pkg in legacy_packages(config):
            print(f"Removing legacy package {pkg}...", end='')
            rmtree(os.path.join(config['package_root'], pkg))
            print("done.")

    print("")

    # Fetch and update packages specified in config file.
    for package_url in config['packages']:
        package_name = package_url.split('/')[-1]
        repo = find_repo(package_url, config['package_root'], args['update_only'])

        # If the repo is null, then the repo either wasn't present or wasn't readable as a Git repo,
        # and this script was running in update-only mode. Either way, skip the next step.
        if repo is None:
            continue

        if not args['install_only']:
            old_commit = repo.head.commit

            print("Refreshing package '{}'...".format(package_name.strip()), end='')
            repo.remotes.origin.pull()
            print("done.".format(package_name))

            if repo.head.commit != old_commit:
                print(f"\tChanges pulled: {repo.head.commit.message}.")

        else:
            print("Install-only mode. Skipping {}.".format(package_name))

    print("\nPackage update done.")


if __name__ == "__main__":
    main()
