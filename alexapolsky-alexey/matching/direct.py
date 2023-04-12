class RegexBase:
    def __init__(self, rest=None):
        self.rest = rest

    def match(self, text):
        for i in range(len(text) + 1):
            if self._match(text, i) is not None:
                return True
        return False

    def _match(self, text, start):
        raise NotImplementedError("derived classes must override '_match'")


class Lit(RegexBase):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def _match(self, text, start):
        next_index = start + len(self.chars)
        if next_index > len(text):
            return None
        if text[start:next_index] != self.chars:
            return None
        if not self.rest:
            return next_index
        return self.rest._match(text, next_index)


class Start(RegexBase):
    def _match(self, text, start):
        if start != 0:
            return None
        return start + 1


class End(RegexBase):
    def _match(self, text, start):
        if start != len(text):
            return None
        return start + 1


class Any(RegexBase):
    def __init__(self, child, rest=None):
        super().__init__(rest)
        self.child = child

    def _match(self, text, start):
        max_possible = len(text) - start
        for num in range(max_possible, -1, -1):
            after_many = self._match_many(text, start, num)
            if after_many is not None:
                return after_many
        return None

    def _match_many(self, text, start, num):
        for i in range(num):
            start = self.child._match(text, start)
            if start is None:
                return None
        if self.rest:
            return self.rest._match(text, start)
        return start


class Alt(RegexBase):
    def __init__(self, patterns, rest=None):
        super().__init__(rest=rest)
        self.patterns = patterns

    def _match(self, text, start):
        for pat in self.patterns:
            after_pat = pat._match(text, start)
            if after_pat is not None:
                if not self.rest:
                    return after_pat
                after_rest = self.rest._match(text, after_pat)
                if after_rest is not None:
                    return after_rest
        return None


class Not(RegexBase):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr

    def _match(self, text, start):
        if self.expr._match(text, start) is None:
            return start + 1
        return None


class Range(RegexBase):
    def __init__(self, start_char, end_char, rest=None):
        super().__init__(rest)
        self.start_char = start_char
        self.end_char = end_char

    def _match(self, text, start):
        next_index = start + 1
        if next_index > len(text):
            return None
        if text[start] < self.start_char or text[start] > self.end_char:
            return None
        if not self.rest:
            return next_index
        return self.rest._match(text, next_index)