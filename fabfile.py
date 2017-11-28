"""
    USAGE: fab deploy
    repo: git@bitbucket.org:mistalaba/ibiza_comunidad.git
"""

import os
# from fabric.api import *
from fabric.api import (
    task, env, prompt, cd, run,
    prefix
)

env.hosts = ['mistalaba@178.62.251.213']
env.user = 'mistalaba'
env.branch = 'default'
env.directory = os.path.dirname(os.path.abspath(__file__))
env.project_name = os.path.basename(env.directory)
env.directory = '/home/mistalaba/projects/%s/' % env.project_name


@task
def update_from_repository():
    branch = prompt("Choose branch to update:", default='master')
    with cd(env.directory):
        with prefix('eval "$(ssh-agent -s)" && ssh-add /home/mistalaba/.ssh/digitalocean_bitbucket'):
            run('git pull origin {}'.format(branch), pty=False)


@task
def update_requirements():
    update_reqs = prompt("Did you make any changes to requirements? (y/n)", default='n')
    if update_reqs == 'y':
        with cd(env.directory), prefix("workon {}".format(env.project_name)):
            run('pip-sync requirements/production_compiled.txt')


@task
def update_database():
    update_db = prompt("Did you make any changes to models? (y/n)", default='n')
    if update_db == 'y':
        with cd(env.directory), prefix("workon {}".format(env.project_name)):
            run("python manage.py migrate --noinput")


@task
def collect_static():
    with cd(env.directory), prefix("workon {}".format(env.project_name)):
        run("python manage.py collectstatic --noinput --clear --verbosity 0")


@task
def supervisord_changes():
    update_supervisord = prompt("Did you make any changes to the Supervisor config? (y/n)", default='n')
    if update_supervisord == 'y':
        run("supervisorctl reread; supervisorctl reload")


@task
def restart_gunicorn():
    run("supervisorctl restart %s" % env.project_name)

@task
def restart_gunicorn_comingsoon():
    update_comingsoon = prompt("Did you make any changes to the comingsoon site? (y/n)", default='n')
    if update_comingsoon == 'y':
        run("supervisorctl restart ibiza_comunidad_comingsoon")

@task
def restart_nginx():
    update_nginx = prompt("Did you make any changes to the Nginx config? (y/n)", default='n')
    if update_nginx == 'y':
        run("service nginx reload")


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
    restart_gunicorn()
    restart_gunicorn_comingsoon()
    restart_celery()
    restart_nginx()
