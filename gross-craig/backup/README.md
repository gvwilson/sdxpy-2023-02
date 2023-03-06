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

### Solution

The code is implemented in `compare_manifests` and tested via the tests
`test_backup.test_compare_*`. The overall approach is to load the manifests
into a dictionary with filenames as keys and lists as values containing the
hashes in the form `[before_hash, after_hash]`. The different entries can be
checked for the conditions listed.

I think that the way to check for renames could definitely be optimized as it
involves a few searches through all files. A more efficient data structure
could be used (potentially sorted on `after_hash`es for faster searches), but
I decided the overhead was not worth it.

One choice that did need to be made is what happens when a file is renamed
(e.g., `mv d.txt b.txt`) and then a new file with that name is created (e.g.,
`touch d.txt`) (see `test_backup.test_compare_delete_add_change` for
details). I think that something like
```bash
d.txt: renamed to b.txt
d.txt: was added
```
is more informative, but potentially more confusing. I decided to go with
```bash
b.txt: added
d.txt: changed
```
as this also allowed for simpler code.

## File history

Write a program called `file_history.py`
that takes the name of a file as a command-line argument
and displays the history of that file
by tracing it back in time through the available manifests.
Again, you can test your program using made-up manifest files.


### Solution

The code is implemented in `file_history` and tested via the tests
`test_backup.test_file_history*`. Much of the code was reused from
`compare_manifests` and therefore moved into the common module
`manifest_utils`. All manifests are loaded and joined so the hashes for each
file are lined up in arrays. These hashes are then searched for changes to be
reported.


## Finding duplicate files

Write a program called `finddup.py` that takes a list of filenames as command-line
arguments, and reports which of those files are duplicates of each other.  The
fastest way to do this is to calculate the hash for each file, and then group files
with the same hashes together. Note that there may be several duplicates of a file,
not just two.

You can test your program by creating a few directories with test files in them
rather than using pyfakefs.

### Solution

The code is implemented in `finddup` and tested via the tests
`test_backup.test_duplicate*`. Files are hashed, and the union of those
hashes are keys of a dictionary pointing to the list of files with those
hashes. Those lists are then printed.
