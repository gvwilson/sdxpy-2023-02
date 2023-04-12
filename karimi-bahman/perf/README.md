Exercises for Dataframe Performance

1.  Look for "FIXME" in `df_col.py` and `df_row.py` and rewrite those
    methods to use loops instead of list comprehensions and dictionary
    comprehensions. (This will help you understand how comprehensions
    work.)

2.  Build a faster dataframe. You can use `DfRow` or `DfCol` as a
    starting point or derive something new from `Dataframe`; whatever
    you choose, modify `timing.py` to import it and collect timing for
    it in the `sweep` function. Remember, the profiler is your friend:
    `profile.sh` shows how to call it for `timing.py` and some sample
    dataframe sizes.
