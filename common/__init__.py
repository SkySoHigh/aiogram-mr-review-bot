from .commands import set_default_commands
from .loader import Loader

__all__ = ['app', 'set_default_commands']

app = Loader()
app.init_db()
