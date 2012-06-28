from fabric import api as fab
from path import path
import os


here = path(__file__)
fabdir = here.parent
projdir = fabdir.parent
srcdir = projdir.parent
venv = path(os.environ['VIRTUAL_ENV'])


@fab.task
def tests():
    rt_dir = srcdir / 'retools'
    for sdir in rt_dir, projdir:
        with fab.lcd(sdir):
            fab.local('nosetests')

