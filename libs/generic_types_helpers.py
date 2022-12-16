import sys
from typing import Any, Tuple

_python_version = sys.version_info

if _python_version >= (3, 8):
    from typing import get_args
else:
    from typing_extensions import get_args


def get_generic_type_arg(cls) -> Tuple[Any]:
    """
    Gets type of arg passed to the typing.Generic
    Args:
        cls: Class object

    Examples:
        ExampleController(BaseController[ExampleModel]) -> returns ExampleModel

    Returns: type of arg passed to the typing.Generic
    """

    t = getattr(cls, '__orig_bases__', None)[0]
    if not t:
        raise KeyError(f'There is no __orig_bases__ in {cls}')
    return get_args(t)
