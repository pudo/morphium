import logging
import warnings
from morphium.archive import env, Archive

warnings.simplefilter("ignore")

fmt = '[%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=fmt)
logging.getLogger('requests').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)
logging.getLogger('alembic').setLevel(logging.WARNING)

__all__ = [env, Archive]
