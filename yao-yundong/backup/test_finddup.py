from pathlib import Path
import pytest
import glob

from finddup import find_dup

@pytest.fixture
def our_fs(fs):
    fs.create_file("a.txt", contents="aaa")
    fs.create_file("b.txt", contents="bbb")
    fs.create_file("sub_dir/c.txt", contents="ccc")
    fs.create_file("d.txt", contents="ccc")
    fs.create_file("e.txt", contents="ccc")
    fs.create_file("f.txt", contents="aaa")

def test_find_dup(our_fs):
    files_lst = ["a.txt", "b.txt", "sub_dir/c.txt", "d.txt", "e.txt", "f.txt"]
    result = find_dup(files_lst)
    assert len(result) == 3
    assert ['b.txt'] in result
    assert ['a.txt', 'f.txt'] in result