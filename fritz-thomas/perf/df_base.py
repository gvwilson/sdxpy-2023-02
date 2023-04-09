class DataFrame:
    """Generic base class for dataframes."""

    def ncol(self):
        """Report the number of columns."""

    def nrow(self):
        """Report the number of rows."""

    def cols(self):
        """Return the set of column names."""

    def get(self, col, row):
        """Get a scalar value."""

    def select(self, *names):
        """Select a subset of columns."""

    def filter(self, func):
        """Select a subset of rows."""

    def eq(self, other):
        """Check equality of two dataframes."""
        assert isinstance(other, DataFrame)
        for n in self.cols():
            if n not in other.cols():
                return False
            for i in range(self.nrow()):
                if self.get(n, i) != other.get(n, i):
                    return False
        return True
