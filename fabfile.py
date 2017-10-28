"""
    USAGE: fab deploy
"""

from fabric.api import *
import os

env.directory = os.path.dirname(os.path.abspath(__file__))
env.project_name = os.path.basename(env.directory)

#server
env.hosts = ['@']


def production():
    env.branch = 'default'
    env.directory = '/home//projects/%s/' % env.project_name
    env.environment = 'production'

#Make production default
production()


def update_from_repository():
    # TODO: Fix for GIT
    branch = prompt("Choose branch to update:", default='default')
    with cd(env.directory):
        run('hg pull; hg update -c --rev %s' % branch)


def update_database():
    update_db = prompt("Did you make any changes to models? (y/n)", default='n')
    if update_db == 'y':
        with cd(env.directory):
            run("workon %s && python manage.py migrate --noinput" % env.project_name)


def collect_static():
    with cd(env.directory):
        run("workon %s && python manage.py collectstatic --noinput --clear" % (env.project_name))


def update_requirements():
    update_reqs = prompt("Did you make any changes to requirements? (y/n)", default='n')
    if update_reqs == 'y':
        with cd(env.directory):
            run("workon %s && pip-sync requirements/production_compiled.txt" % env.project_name)


@task
def restart_webfaction():
    run("supervisorctl restart %s" % env.project_name)


@task
def supervisord_changes():
    update_supervisord = prompt("Did you make any changes to the Supervisor config? (y/n)", default='n')
    if update_supervisord == 'y':
        run("supervisorctl reread; supervisorctl update")


@task
def restart_nginx():
    update_nginx = prompt("Did you make any changes to the Nginx config? (y/n)", default='n')
    if update_nginx == 'y':
        run("supervisorctl restart nginx")


@task
def restart_celery():
    update_celery = prompt("Did you make any changes to the Celery tasks? (y/n)", default='n')
    if update_celery == 'y':
        run("supervisorctl restart celery")


@task(default=True)
def deploy(mode=None):
    update_from_repository()
    update_requirements()
    update_database()
    collect_static()
    supervisord_changes()
    restart_webfaction()
    restart_celery()
    restart_nginx()
