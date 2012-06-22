#

def test_loadtasks():
    from ltweb.app import load_tasks_list
    out = load_tasks_list('ltweb.tests.dummytasks')
    assert all(x in out[0] for x in ('path', 'name', 'desc'))
    

