from StringIO import StringIO

class Tee(object):
    """
    from http://bit.ly/uKuUpu
    """
    sys_handle = None
    teed = True
    def __init__(self, fh=None):
        import sys
        out = getattr(sys, self.sys_handle)
        self.file = fh and fh or StringIO()
        self.out = out

    def set(self):
        import sys
        setattr(sys, self.sys_handle, self)
        del sys
        return self

    def __del__(self):
        import sys
        setattr(sys, self.sys_handle, self.out)
        self.file.flush()
        self.file.close()
        del sys
        del self

    def write(self, data):
        self.out.write(data)
        self.file.write(data)



class sysout(Tee):
    sys_handle = 'stdout'


class syserr(Tee):
    sys_handle = 'stderr'
