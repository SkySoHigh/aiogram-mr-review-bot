from __future__ import unicode_literals

import sys
from reprlib import Repr as _Repr

from sqlalchemy import inspect
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import declarative_base


class Repr(_Repr):
    def repr(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            return self.repr_Base(obj, self.maxlevel)
        if sys.version_info < (3,):
            return _Repr.repr(self, obj)
        else:
            return super(Repr, self).repr(obj)

    def repr_Base(self, obj, level):
        return '<%s %s>' % (self._repr_class(obj, level),
                            self._repr_attrs(obj, level))

    def _repr_class(self, obj, level):
        return obj.__class__.__name__

    def _repr_attrs(self, obj, level):
        represented_attrs = []
        for attr in self._iter_attrs(obj):
            represented_attr = self._repr_attr(attr, level)
            represented_attrs.append(represented_attr)
        return ', '.join(represented_attrs)

    def _repr_attr(self, obj, level):
        attr_name, attr_value = obj
        if hasattr(attr_value, 'isoformat'):
            return '%s=%r' % (attr_name, attr_value.isoformat())
        return '%s=%r' % (attr_name, attr_value)

    def _iter_attrs(self, obj):
        blacklist = set(getattr(obj, '__repr_blacklist__', set()))
        whitelist = set(getattr(obj, '__repr_whitelist__', set()))

        attr_names = inspect(obj.__class__).columns.keys()
        for attr_name in attr_names:
            if attr_name in blacklist:
                continue

            if whitelist and attr_name not in whitelist:
                continue

            yield (attr_name, getattr(obj, attr_name))


_shared_repr = Repr()


class RepresentableBase(object):
    def __repr__(self):
        return _shared_repr.repr(self)


Base = declarative_base(cls=RepresentableBase)
