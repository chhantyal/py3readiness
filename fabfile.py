import os
from contextlib import contextmanager
from fabric.api import env, run, local, prefix, sudo


def live():
    """Connects to the server."""
    env.hosts = [os.environ.get('py3_hosts', 'u6.uhura.de')]
    env.user = os.environ.get('py3_user', 'uhura')
    env.cwd = '/var/www/py3readiness.org'
    env.connect_to = '{0}@{1}:{2}'.format(env.user, env.hosts[0], env.cwd)


def gitpull(tag=None):
    """Pulls upstream brunch on the server."""
    if tag is not None:
        run('git pull')
        run('git checkout %s' % tag)
    else:
        run('git pull')


@contextmanager
def source_env():
    """Actives embedded virtual env"""
    with prefix('source env/bin/activate'):
        yield


def install_requirements():
    """Installs requirements inside vertualenv"""
    with source_env():
        run('pip install --force-reinstall -Ur requirements.txt')


def generate():
    """Generates updates using generate.py script"""
    with source_env():
        run('python generate.py')


def update(tag=None):
    """Updates changes in server (might restart webserver)"""
    gitpull()
    install_requirements()
    generate()