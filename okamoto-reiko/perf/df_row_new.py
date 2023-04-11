import inspect

from df_base import DataFrame
from util import dict_match

class DfRowNew(DataFrame):
    """A row-oriented dataframe."""

    def __init__(self, rows):
        """Construct dataframe from a list of dictionaries."""
        assert len(rows) > 0
        assert all(dict_match(r, rows[0]) for r in rows)
        self._data = rows

    def __str__(self):
        return str(self._data)

    def ncol(self):
        return len(self._data[0])

    def nrow(self):
        return len(self._data)

    def cols(self):
        return set(self._data[0].keys())

    def get(self, col, row):
        assert col in self._data[0]
        assert 0 <= row < len(self._data)
        return self._data[row][col]

    def select(self, *names):
        """FIXME: rewrite this using loops."""
        #assert all(n in self._data[0] for n in names)
        for n in names:
            assert n in self._data[0]
        #rows = [{key: r[key] for key in names} for r in self._data]
        rows = {}
        for key in names:
            rows[key] = []
        for r in self._data:
            for key in names:
                rows[key].append(r[key])   
        return DfRowNew([rows])

    def filter(self, func):
        """FIXME: rewrite this using loops."""
        #params = list(inspect.signature(func).parameters.keys()) # only modification I'm making for exercise 2
        #result = [r for r in self._data if func(**r)]
        result = []
        for r in self._data:
            if func(**r):
                result.append(r)
        return DfRowNew(result)
