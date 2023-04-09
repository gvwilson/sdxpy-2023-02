import inspect

from df_base import DataFrame
from util import all_eq

class DfCol(DataFrame):
    """A column-oriented dataframe."""

    def __init__(self, **kwargs):
        """Construct dataframe from a dictionary of lists."""
        assert len(kwargs) > 0
        assert all_eq(len(kwargs[k]) for k in kwargs)
        for k in kwargs:
            assert all_eq(type(v) for v in kwargs[k])
        self._data = kwargs

    def __str__(self):
        return str(self._data)

    def ncol(self):
        return len(self._data)

    def nrow(self):
        n = list(self._data.keys())[0]
        return len(self._data[n])

    def cols(self):
        return set(self._data.keys())

    def get(self, col, row):
        assert col in self._data
        assert 0 <= row < len(self._data[col])
        return self._data[col][row]

    def select(self, *names):
        """FIXME: rewrite this using loops."""
        assert all(n in self._data for n in names)
        return DfCol(**{n: self._data[n] for n in names})

    def filter(self, func):
        """FIXME: rewrite this using loops."""
        params = list(inspect.signature(func).parameters.keys())
        result = {n: [] for n in self._data}
        for i in range(self.nrow()):
            args = {n: self._data[n][i] for n in self._data}
            if func(**args):
                for n in self._data:
                    result[n].append(self._data[n][i])
        return DfCol(**result)
