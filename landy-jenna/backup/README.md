Note: the lesson for this week covered both the backup tool and how to use mock objects
like pyfakefs in testing. It was clearly too much material—my apologies for trying to
cram it all in—so the exercises below do _not_ require you to use pyfakefs. I will put
together an entire lesson on mock objects to run later in the course.

## Comparing manifests

Write a program `compare-manifests.py` that reads two manifest files and reports:

-   Which files have the same names but different hashes
    (i.e., their contents have changed).
-   Which files have the same hashes but different names
    (i.e., they have been renamed).
-   Which files are in the first hash but neither their names nor their hashes are in the second
    (i.e., they have been deleted).
-   Which files are in the second hash but neither their names nor their hashes are in the first
    (i.e., they have been added).

You can test your program by hand-writing a few manifest CSV files with made-up hashes.

## File history

Write a program called `file_history.py`
that takes the name of a file as a command-line argument
and displays the history of that file
by tracing it back in time through the available manifests.
Again, you can test your program using made-up manifest files.

## Finding duplicate files

Write a program called `finddup.py` that takes a list of filenames as command-line
arguments, and reports which of those files are duplicates of each other.  The
fastest way to do this is to calculate the hash for each file, and then group files
with the same hashes together. Note that there may be several duplicates of a file,
not just two.

You can test your program by creating a few directories with test files in them
rather than using pyfakefs.
