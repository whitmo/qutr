from StringIO import StringIO

class Tee(object):
    """
    from http://bit.ly/uKuUpu
    """
    sys_handle = None
    
    def __init__(self, fh=None):
        import sys
        self.file = fh and fh or StringIO()
        self.out = getattr(sys, self.sys_handle)
        setattr(sys, self.sys_handle, self)
        del sys

    def __del__(self):
        import sys
        setattr(sys, self.sys_handle, self.out)
        self.file.flush()
        self.file.close()
        del sys
        del self

    def write(self, data):
        self.file.write(data)
        self.out.write(data)


class sysout(Tee):
    sys_handle = 'stdout'


class syserr(Tee):
    sys_handle = 'stderr'
