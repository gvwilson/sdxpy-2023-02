# Code attribution: Greg Wilson's slides 
class Match:
    def __init__(self, rest):
        self.rest = rest if rest is not None else Null()
        
    def match(self, text):
        result = self._match(text, 0)
        return result == len(text)
    
class Null(Match):
    def __init__(self, rest=None):
        self.rest = None
        
    def _match(self, text, start):
        return start
    
class Lit(Match):
    def __init__(self, chars, rest=None):
        super().__init__(rest)
        self.chars = chars
    def _match(self, text, start):
        end = start + len(self.chars)
        if text[start:end] != self.chars:
            return None
        return self.rest._match(text, end)
    
class Any(Match):
    def __init__(self, rest=None):
        super().__init__(rest)
    def _match(self, text, start):
        for i in range(len(text) + 1):
            end = self.rest._match(text, i)
            if end == len(text):
                return end
        return None    

# Question 1 ----------

class Not:
    def __init__(self, rest):
        self.rest = rest
        
    def match(self, text):
        return not self.rest.match(text)
    
# Tests for question 1 (adapted from slides)

def test_literal_match_entire_string():
    # ⌈abc⌋ ≈ "abc"
    assert not Not(Lit("abc")).match("abc")
    
def test_literal_substring_alone_no_match():
    # ⌈ab⌋ ≉ "abc"
    assert Not(Lit("ab")).match("abc")

def test_literal_superstring_no_match():
    # ⌈abc⌋ ≉ "ab"
    assert Not(Lit("abc")).match("ab")
    
def test_literal_followed_by_literal_match():
    # ⌈a⌋⌈b⌋ ≈ "ab"
    assert not Not(Lit("a", Lit("b"))).match("ab")

def test_literal_followed_by_literal_no_match():
    # ⌈a⌋⌈b⌋ ≉ "ac"
    assert Not(Lit("a", Lit("b"))).match("ac")
    
def test_any_matches_empty():
    # ⌈*⌋ ≈ ""
    assert not Not(Any()).match("")
    
def test_any_matches_entire_string():
    # ⌈*⌋ ≈ "abc"
    assert not Not(Any()).match("abc")
    
# Question 2 ----------

class Range(Match):
    def __init__(self, first, last, rest=None):
        super().__init__(rest)
        self.first = first
        self.last = last

    def _match(self, text, start):
        end = start + 1
        for pat in range(ord(self.first), ord(self.last)+1):
            if text == chr(pat):
                return self.rest._match(text, end)
            
# Tests for question 2 

def test_first_letter_range():
     # ⌈a-c⌋ ≈ "a"
    assert Range("a", "c").match("a")
    
def test_middle_letter_range():
     # ⌈a-c⌋ ≈ "b"
    assert Range("a", "c").match("b")
    
def test_last_letter_range():
     # ⌈a-c⌋ ≈ "b"
    assert Range("a", "c").match("c")
    
def test_letter_outside_range_no_match():
     # ⌈a-c⌋ ≈ "d"
    assert not Range("a", "c").match("d")
    
def test_letter_outside_range_no_match():
     # ⌈a-c⌋ ≉  "d"
    assert not Range("a", "c").match("d")
    
def test_text_not_single_letter():
     # ⌈a-c⌋ ≉  "ab"
    assert not Range("a", "c").match("ab")
    
# Question 3 ----------

class Either(Match):
    def __init__(self, patterns=[Null()], rest=None):
        super().__init__(rest)
        self.patterns = patterns if patterns is not None else [Null()]
        
    def _match(self, text, start):
        for pat in self.patterns:
            end = pat._match(text, start)
            if end is not None:
                end = self.rest._match(text, end)
                if end == len(text):
                    return end
        return None
    
# Tests for question 3

def test_either_two_literals_first():
    # ⌈{a,b}⌋ ≈ "a"
    assert Either([Lit("a"), Lit("b")]).match("a")
def test_either_two_literals_second():
    # ⌈{a,b}⌋ ≈ "b"
    assert Either([Lit("a"), Lit("b")]).match("b")
def test_either_two_literals_neither():
    # ⌈{a,b}⌋ ≉ "c"
    assert not Either([Lit("a"), Lit("b")]).match("c")
def test_either_two_literals_not_both():
    # ⌈{a,b}⌋ ≉ "ab"
    assert not Either([Lit("a"), Lit("b")]).match("ab")
def test_either_three():
    # ⌈{a,b,c}⌋ ≈ "b"
    assert Either([Lit("a"), Lit("b"), Lit("c")]).match("b")
    
# When no sub-patterns are specified, self.patterns defaults to [Null()]
    