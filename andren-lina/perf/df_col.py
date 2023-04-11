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
        #assert all(n in self._data for n in names)
        # i can probably redo it with loops in at least three other ways that would look better but this is a minimal change that should still work. 
        lista = list()
        for n in names:
            lista.append(n in self._data)
        assert all(lista)
        #return DfCol(**{n: self._data[n] for n in names})
        my_dict = {}
        for n in names:
            my_dict[n] = self._data[n]
        return DfCol(**my_dict)

    def filter(self, func):
        """FIXME: rewrite this using loops."""
        params = list(inspect.signature(func).parameters.keys())
        #result = {n: [] for n in self._data}
        result = {}
        for n in self._data:
            result[n] = []
        for i in range(self.nrow()):
            #args = {n: self._data[n][i] for n in self._data}
            args = {}
            for n in self._data:
                args[n] = self._data[n][i]  
            if func(**args):
                for n in self._data:
                    result[n].append(self._data[n][i])
        return DfCol(**result)
    # those are all extremely automatic rewrites. I'm far to tired right now to even try to understand what the code is doing, but I believe I can still do the rewrites on autopilot. i'm a mathematician by training and my first programing language was Haskell so i suppose i'm just weird :)
