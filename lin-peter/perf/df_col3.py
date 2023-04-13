import inspect

from df_base import DataFrame
from util import all_eq

import multiprocessing as mp

class DfCol3(DataFrame):
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

    def check_column(self, name, data):
        assert name in data
        return (name, data[name])

    def select(self, *names):
        selected_data = {}
        with mp.Pool() as pool:
            results = []
            for n in names:
                result = pool.apply_async(
                    self.check_column,
                    args=(n, self._data)
                )
                results.append(result)
            for result in results:
                # unpack result object
                col_name, col_data = result.get()
                selected_data[col_name] = col_data

        return DfCol3(**selected_data)

    def filter(self, func):
        """FIXME: rewrite this using loops."""
        params = list(inspect.signature(func).parameters.keys())
        # result = {n: [] for n in self._data}
        result = {}
        for n in self._data:
            result[n] = []

        for i in range(self.nrow()):
            args = {}
            for n in self._data:
                args[n] = self._data[n][i]
            # args = {n: self._data[n][i] for n in self._data}
            if func(**args):
                for n in self._data:
                    result[n].append(self._data[n][i])
        return DfCol3(**result)
