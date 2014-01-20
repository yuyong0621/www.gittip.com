#!/usr/bin/env python
"""\
Gittip
~~~~~~

A personal funding platform.

Dependencies:
- Python 2.7
- Postgresql 9.2

To run:
$ gittip.py

This will also initialize a local environment on the first run.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import hashlib
import os
import sys
import shutil
from subprocess import check_call, check_output, STDOUT, CalledProcessError


is_win = sys.platform.startswith('win')
bin_dir = 'Scripts' if is_win else 'bin'
ext = '.exe' if is_win else ''

vendor_path = 'vendor'
env_path = 'env'
requirements_installed_path = os.path.join(env_path, '.requirements_installed')
bin_path = os.path.join(env_path, bin_dir)
default_config_path = 'default_local.env'
virtualenv_path = os.path.join(vendor_path, 'virtualenv-1.9.1.py')
pip_path = os.path.join(bin_path, 'pip' + ext)
swaddle_path = os.path.join(bin_path, 'swaddle' + ext)
aspen_path = os.path.join(bin_path, 'aspen' + ext)


def main():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--port', '-p', type=int, default=8537, help='port to listen to')
    parser.add_argument('--config', '-c', default='local.env', help='configuration filepath')
    parser.add_argument('--address', '-a', default='localhost', help='address to listen to')
    parser.add_argument('--version', action='version', version='ahoj')
    parser.add_argument('--clean', action='store_true', help='clean env')
    #parser.add_argument('command', nargs='?', default='run', help='what to do')
    args = parser.parse_args()

    try:
        bootstrap_environment(args)
    except CalledProcessError as ex:
        print(ex.output)
    except EnvironmentError as ex:
        print('Error:', ex)
        return 1

    run_server(args)


def bootstrap_environment(args):
    ensure_dependencies(args)
    init_config(args)
    init_virtualenv(args)
    install_requirements(args)


def ensure_dependencies(args):
    if not shell('python', '--version', capture=True).startswith('Python 2.7'):
        raise EnvironmentError('Python 2.7 is required.')

    try:
        shell('pg_config' + ext, capture=True)
    except OSError as e:
        if e.errno != os.errno.ENOENT:
            raise
        raise EnvironmentError('Postgresql is required. (Make sure pg_config is on your PATH.)')


def init_config(args):
    if os.path.exists(args.config):
        return

    print('Creating a %s file...' % args.config)
    shutil.copyfile(default_config_path, args.config)


def init_virtualenv(args):
    if os.path.exists(env_path):
        return

    print('Initializing virtualenv at %s...' % env_path)

    shell('python', virtualenv_path,
          '--unzip-setuptools',
          '--prompt="[gittip] "',
          '--never-download',
          '--extra-search-dir=' + vendor_path,
          '--distribute',
          env_path)


def install_requirements(args):

    with open('requirements.txt', 'rb') as f:
        req = f.read()
    with open('requirements_tests.txt', 'rb') as f:
        req += f.read()

    try:
        with open(requirements_installed_path, 'rb') as f:
            old_hash = f.read()
    except IOError:
        old_hash = ''

    new_hash = hashlib.sha1(req).hexdigest()

    if not args.clean and old_hash == new_hash:
        return

    print('Installing requirements...')

    shell(pip_path, 'install', '-r', 'requirements.txt')
    shell(pip_path, 'install', '-r', 'requirements_tests.txt')
    shell(pip_path, 'install', '-e', '.')

    with open(requirements_installed_path, 'w') as f:
        f.write(new_hash)


def run_server(args):

    try:
        shell(swaddle_path, args.config, aspen_path,
            '--www_root=www/',
            '--project_root=.',
            '--show_tracebacks=yes',
            '--changes_reload=yes',
            '--network_address=%s:%s' % (args.address, args.port))
    except KeyboardInterrupt:
        pass


def shell(*args, **kwargs):
    if kwargs.pop('capture', None):
        return check_output(args, stderr=STDOUT, **kwargs)
    return check_call(args, **kwargs)


if __name__ == '__main__':
    sys.exit(main())
