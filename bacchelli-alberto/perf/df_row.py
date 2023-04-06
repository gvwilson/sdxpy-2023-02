import inspect

from df_base import DataFrame
from util import dict_match

class DfRow(DataFrame):
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
        assert all(n in self._data[0] for n in names)
        rows = [{key: r[key] for key in names} for r in self._data]
        return DfRow(rows)

    def filter(self, func):
        """FIXME: rewrite this using loops."""
        params = list(inspect.signature(func).parameters.keys())
        result = [r for r in self._data if func(**r)]
        return DfRow(result)
