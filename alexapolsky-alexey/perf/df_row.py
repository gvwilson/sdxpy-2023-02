import inspect
import numpy
# [top]
from functools import cache

from df_base import DataFrame
from util import dict_match

class DfRow(DataFrame):
    def __init__(self, rows):
        assert len(rows) > 0
        assert all(dict_match(r, rows[0]) for r in rows)
        self._data = numpy.array(rows)
    # [/top]

    # [simple]
    def ncol(self):
        return len(self._data[0].keys())

    def nrow(self):
        return len(self._data)

    def cols(self):
        return set(self._data[0].keys())
    # [/simple]

    # [equal]
    def eq(self, other):
        assert isinstance(other, DataFrame)
        for (i, row) in enumerate(self._data):
            for key in row:
                if key not in other.cols():
                    return False
                if row[key] != other.get(key, i):
                    return False
        return True
    # [/equal]

    # [get]
    def get(self, col, row):
        assert col in self._data[0]
        assert 0 <= row < len(self._data)
        return self._data[row][col]
    # [/get]

    # [select]
    def select(self, *names):
        assert all(n in self._data[0] for n in names)
        # rows = [{key: r[key] for key in names} for r in self._data]
        rows = []
        for r in self._data:
            new_r = {}
            for key in names:
                new_r[key] = r[key]
            rows.append(new_r)
        return DfRow(rows)
    # [/select]

    # [filter]
    def filter(self, func):
        params = list(inspect.signature(func).parameters.keys())
        # result = [r for r in self._data if func(**r)]
        result = []

        @cache
        def cache_func(**r):
            return func(**r)

        for r in self._data:
            if cache_func(**r):
                result.append(r)
        return DfRow(result)
    # [/filter]

    def __str__(self):
        return str(self._data)
