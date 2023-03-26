## Exclusion

1.  Create a matcher that *doesn't* match a specified pattern.
    For example, `Not(Lit("abc"))` only succeeds if the text isn't "abc".

2.  Write some tests for it.

## Ranges

1.  Create a matcher that matches a range of characters.
    For example, `Range("a", "z")` matches any single lower-case Latin alphabetic character.
    (This is just a convenience matcher: ranges can always be spelled out in full.)

2.  Write some tests for it.

## Multiple Alternatives

1.  Modify `Either` so that it can match any number of sub-patterns, not just two.

2.  Write some tests for it.

3.  What does your implementation do when no sub-patterns are specified?
