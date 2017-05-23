import os

TAG_LATEST = 'latest'


def env(name, default=None):
    """Get an envvar either from the morph namespace or the original name."""
    name = name.upper()
    mname = 'MORPH_' + name.upper()
    return os.environ.get(mname, os.environ.get(name, default))
