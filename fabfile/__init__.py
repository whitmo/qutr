from fabric import api as fab
from path import path
import os


here = path(__file__)
fabdir = here.parent
projdir = fabdir.parent
docdir = projdir / 'doc'
srcdir = projdir.parent
venv = path(os.environ['VIRTUAL_ENV'])


@fab.task
def test(stats='', commit=False):
    rt_dir = srcdir / 'retools'
    results = []
    for sdir in rt_dir, projdir:
        with fab.lcd(sdir):
            metdir = docdir / 'metrics' / sdir.name
            if not metdir.exists():
                metdir.makedirs()
            if stats:
                stats = " --with-xunit"
                " --xunit-file={xunit}"
                " --cover-html"
                " --cover-html-dir={coverage}".format(xunit=metdir / "xunit.xml",
                                                      coverage=metdir)
            runner = 'nosetests -vv{stats}'.format(stats=stats) 
            out = fab.local(runner)
            results.append(out)
            if commit:
                fab.local('git add %s' %metdir)
                fab.local('git commit -m "<doc:testrun>"')
    return all(res.succeeded for res in results)


@fab.task            
def push(remote='origin', branch='master'):
    with fab.settings(warn_only=True):
        if test() is True:
            fab.local("git push {remote} {branch}".format(locals()))
