class RegexBase:
    def __init__(self, rest=None):
        self.rest = rest
    # text: "fadfg"
    def match(self, text):
        for i in range(len(text) + 1): # 5
            if self._match(text, i) is not None:
                return True
        return False

    def _match(self, text, start):
        raise NotImplementedError("derived classes must override '_match'")

class Lit(RegexBase):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars
    # text: "fadfg" start: 0
    def _match(self, text, start):
        next_index = start + len(self.chars) # 0 + 3
#         print(next_index, self.rest, text, text[start:next_index])
        if next_index > len(text):
            return None
        if text[start:next_index] != self.chars:
            return None
        if not self.rest:
#             print(self.rest, next_index)
            return next_index
        return self.rest._match(text, next_index)

class Not(RegexBase):
    def __init__(self, child, rest=None):
        super().__init__(rest)
        self.child = child
    def _match(self, text, start):
        next_index = start + len(self.child.chars)
        if next_index > len(text):
            return None
        if self.child._match(text, start) is None:
            if not self.rest:
                return start
            return self.rest._match(text, next_index)
        return None

    
assert not Not(Lit("abc")).match("")
assert not Not(Lit("abc")).match("abc")
assert Not(Lit("abc")).match("def")

assert not Not(Lit("")).match("abc")
assert not Not(Lit("")).match("")


class Range(RegexBase):
    def __init__(self, start, end, rest=None):
        super().__init__(rest)
        self.start = start
        self.end = end

    def _match(self, text, start):
        if start >= len(text):
            return None
        if self.start <= text[start] <= self.end:
            if not self.rest:
                return start+1
            return self.rest._match(text, start+1)
        return None

pattern = Range('a', 'z')
assert pattern.match('abc123')
assert not pattern.match('123')

class Either(RegexBase):
    def __init__(self, *patterns, rest=None):
        super().__init__(rest)
        self.patterns = patterns

    def _match(self, text, start):
        for pattern in self.patterns:  # just loop one step if no sub-patterns are specified.
            after_pattern = pattern._match(text, start)
            if after_pattern is not None:
                if not self.rest:
                    return after_pattern
                after_rest = self.rest._match(text, after_pattern)
                if after_rest is not None:
                    return after_rest
        return None
    
pattern = Either(Lit("hello"), Lit("world"), Lit("!"))
assert pattern.match("hello")   
assert pattern.match("world")  
assert pattern.match("!")      
assert not pattern.match("foo")    