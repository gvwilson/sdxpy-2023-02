class Match:
    def __init__(self, rest):
        self.rest = rest if rest is not None else Null()

    def match(self, text):
        result = self._match(text, 0)
        return result == len(text)

    def _match(self, text, start=0):
        raise "Must implement _match"


class Null(Match):
    def __init__(self, rest=None):
        self.rest = None

    def _match(self, text, start):
        return start


class Lit(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars

    def _match(self, text, start=0):
        end = start + len(self.chars)
        if text[start:end] != self.chars:
            return None
        return self.rest._match(text, end)


class Not(Match):
    def __init__(self, left, rest=None):
        super().__init__(rest)
        self.left = left

    def _match(self, text, start=0):
        for pat in [self.left]:
            end = pat._match(text, start)
            if end is None:
                # use length of pattern chars (if exists)
                if pat.chars:
                    end = start + len(pat.chars)
                end = self.rest._match(text, end)
                if end == len(text):
                    return end
        return None


class Any(Match):
    def __init__(self, rest=None):
        super().__init__(rest)

    def _match(self, text, start=0):
        for i in range(start, len(text) + 1):
            end = self.rest._match(text, i)
            if end == len(text):
                return end
        return None


class Either(Match):
    def __init__(self, left, right, rest=None):
        super().__init__(rest)
        self.left = left
        self.right = right

    def _match(self, text, start=0):
        for pat in [self.left, self.right]:
            end = pat._match(text, start)
            if end is not None:
                end = self.rest._match(text, end)
                if end == len(text):
                    return end
        return None
