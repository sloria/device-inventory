"""
Starter fabfile for deploying the inventory project.

Change all the things marked CHANGEME. Other things can be left at their
defaults if you are happy with the default layout.
"""

import posixpath

from fabric.api import run, local, env, settings, cd, task
from fabric.contrib.files import exists
from fabric.operations import _prefix_commands, _prefix_env_vars
#from fabric.decorators import runs_once
#from fabric.context_managers import cd, lcd, settings, hide

# CHANGEME
env.hosts = ['user@inventory.example.com']
env.code_dir = '/srv/www/inventory'
env.project_dir = '/srv/www/inventory/inventory'
env.static_root = '/srv/www/inventory/static/'
env.virtualenv = '/srv/www/inventory/.virtualenv'
env.code_repo = 'git@github.com:sloria/inventory.git'
env.django_settings_module = 'inventory.settings'

# Python version
PYTHON_BIN = "python2.7"
PYTHON_PREFIX = ""  # e.g. /usr/local  Use "" for automatic
PYTHON_FULL_PATH = "%s/bin/%s" % (PYTHON_PREFIX, PYTHON_BIN) if PYTHON_PREFIX else PYTHON_BIN

# Set to true if you can restart your webserver (via wsgi.py), false to stop/start your webserver
# CHANGEME
DJANGO_SERVER_RESTART = False


def virtualenv(venv_dir):
    """
    Context manager that establishes a virtualenv to use.
    """
    return settings(venv=venv_dir)


def run_venv(command, **kwargs):
    """
    Runs a command in a virtualenv (which has been specified using
    the virtualenv context manager
    """
    run("source %s/bin/activate" % env.virtualenv + " && " + command, **kwargs)


def install_dependencies():
    ensure_virtualenv()
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            run_venv("pip install -r requirements/prod.txt")


def ensure_virtualenv():
    if exists(env.virtualenv):
        return

    with cd(env.code_dir):
        run("virtualenv --no-site-packages --python=%s %s" %
            (PYTHON_BIN, env.virtualenv))
        run("echo %s > %s/lib/%s/site-packages/projectsource.pth" %
            (env.project_dir, env.virtualenv, PYTHON_BIN))


def ensure_src_dir():
    if not exists(env.code_dir):
        run("mkdir -p %s" % env.code_dir)
    with cd(env.code_dir):
        if not exists(posixpath.join(env.code_dir, '.git')):
            run('git clone %s .' % (env.code_repo))


def push_sources():
    """
    Push source code to server
    """
    ensure_src_dir()
    local('git push origin master')
    with cd(env.code_dir):
        run('git pull origin master')


@task
def run_tests():
    """ Runs the Django test suite as is.  """
    local("./manage.py test")


@task
def version():
    """ Show last commit to the deployed repo. """
    with cd(env.code_dir):
        run('git log -1')


@task
def uname():
    """ Prints information about the host. """
    run("uname -a")


@task
def webserver_stop():
    """
    Stop the webserver that is running the Django instance
    """
    run("service apache2 stop")


@task
def webserver_start():
    """
    Starts the webserver that is running the Django instance
    """
    run("service apache2 start")


@task
def webserver_restart():
    """
    Restarts the webserver that is running the Django instance
    """
    if DJANGO_SERVER_RESTART:
        with cd(env.code_dir):
            run("touch %s/wsgi.py" % env.project_dir)
    else:
        with settings(warn_only=True):
            webserver_stop()
        webserver_start()


def restart():
    """ Restart the wsgi process """
    with cd(env.code_dir):
        run("touch %s/inventory/wsgi.py" % env.code_dir)


def build_static():
    assert env.static_root.strip() != '' and env.static_root.strip() != '/'
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            run_venv("./manage.py collectstatic -v 0 --clear --noinput")

    run("chmod -R ugo+r %s" % env.static_root)


@task
def first_deployment_mode():
    """
    Use before first deployment to switch on fake south migrations.
    """
    env.initial_deploy = True


@task
def update_database(app=None):
    """
    Update the database (run the migrations)
    Usage: fab update_database:app_name
    """
    with virtualenv(env.virtualenv):
        with cd(env.code_dir):
            if getattr(env, 'initial_deploy', False):
                run_venv("./manage.py syncdb --all")
                run_venv("./manage.py migrate --fake --noinput")
            else:
                run_venv("./manage.py syncdb --noinput")
                if app:
                    run_venv("./manage.py migrate %s --noinput" % app)
                else:
                    run_venv("./manage.py migrate --noinput")


@task
def sshagent_run(cmd):
    """
    Helper function.
    Runs a command with SSH agent forwarding enabled.

    Note:: Fabric (and paramiko) can't forward your SSH agent.
    This helper uses your system's ssh to do so.
    """
    # Handle context manager modifications
    wrapped_cmd = _prefix_commands(_prefix_env_vars(cmd), 'remote')
    try:
        host, port = env.host_string.split(':')
        return local(
            "ssh -p %s -A %s@%s '%s'" % (port, env.user, host, wrapped_cmd)
        )
    except ValueError:
        return local(
            "ssh -A %s@%s '%s'" % (env.user, env.host_string, wrapped_cmd)
        )


@task
def deploy():
    """
    Deploy the project.
    """
    with settings(warn_only=True):
        webserver_stop()
    push_sources()
    install_dependencies()
    update_database()
    build_static()
    webserver_start()

@task
def watchmedo():
    """
    Watches the file system for changes of ``*.py`` files and executes the tests
    whenever you save a file.
    """ 
    cmd = "watchmedo shell-command --recursive --ignore-directories --patterns='*.py' --wait --command='fab test:integration=1,selenium=0' ."
    local(cmd)

@task
def test(unit=1, integration=1, functional=1, selenium=0, all=0):
    """
    Central command for running tests.
    NOTE: integration and functional tests are included by default.
    Selenium tests are not.

    Call it like so:
        >> fab test
        This will run unit, integration (views tests), and functional (webtest) tests.

        To run selenium tests selenium tests only, 
        >> fab test:selenium=1 

        To run all tests,
        >> fab test:all=1
    """
    command = './manage.py test -v 2 --settings=inventory.settings.test_settings'
    if all == 0:
        if int(unit) == 0:
            command += " --exclude='unit_tests' "
        if int(integration) == 0:
            command += " --exclude='integration_tests' "
        if int(functional) == 0:
            command += " --exclude='functional_tests' "
        if int(selenium) == 0:
            command += ' --exclude="selenium_tests" '
    local(command)
