import pytest
import csv
import manifest_utils
import compare_manifests
import file_history
import finddup


@pytest.fixture()
def csv_manifests(tmp_path):
    """Save sample manifest csv to the tmp_path directory

    Parameters
    ----------
    tmp_path : temporary directory fixture from pytest

    Returns
    -------
    list of paths of sample manifests

    """
    manifests = {}
    manifests[tmp_path / "0000000000.csv"] = \
        ["filename,hash",
         "a.txt,abc123"]
    manifests[tmp_path / "0000000001.csv"] = \
        ["filename,hash",
         "a.txt,abc123",
         "b.txt,def456"]
    manifests[tmp_path / "0000000002.csv"] = \
        ["filename,hash",
         "a.txt,def456"]
    manifests[tmp_path / "0000000003.csv"] = \
        ["filename,hash",
         "b.txt,abc123"]
    manifests[tmp_path / "0000000004.csv"] = \
        ["filename,hash",
         "a.txt,abc123",
         "b.txt,def456",
         "c.txt,ghi789"]
    manifests[tmp_path / "0000000005.csv"] = \
        ["filename,hash",
         "a.txt,abc123",
         "d.txt,def456",
         "e.txt,jkl101"]
    manifests[tmp_path / "0000000006.csv"] = \
        ["filename,hash",
         "b.txt,def456",
         "d.txt,mno112",
         "e.txt,jkl101"]
    for path, manifest in manifests.items():
        with open(path, 'w', newline='') as file:
            file.write("\n".join(manifest))
    yield sorted(manifests.keys())
    for path in manifests.keys():
        path.unlink()


@pytest.fixture()
def text_files(tmp_path):
    """Save sample text_files to the tmp_path directory

    Parameters
    ----------
    tmp_path : temporary directory fixture from pytest

    Returns
    -------
    list of paths of sample text files

    """
    text_files = {}
    text_files[tmp_path / "a.txt"] = ["a"]
    text_files[tmp_path / "b.txt"] = ["b"]
    text_files[tmp_path / "c.txt"] = ["a"]
    text_files[tmp_path / "d.txt"] = ["a"]
    text_files[tmp_path / "e.txt"] = ["b"]
    text_files[tmp_path / "f.txt"] = ["c"]
    text_files[tmp_path / "g.txt"] = ["c"]
    for path, text_file in text_files.items():
        with open(path, 'w', newline='') as file:
            file.write("\n".join(text_file))
    yield sorted(text_files.keys())
    for path in text_files.keys():
        path.unlink()


def test_read_manifests(csv_manifests):
    manifest_dict = manifest_utils.read_manifest(csv_manifests[4])
    assert len(manifest_dict.keys()) == 3
    assert "a.txt" in manifest_dict.keys()
    assert manifest_dict["a.txt"] == "abc123"
    assert "b.txt" in manifest_dict.keys()
    assert manifest_dict["b.txt"] == "def456"
    assert "c.txt" in manifest_dict.keys()
    assert manifest_dict["c.txt"] == "ghi789"


def test_join_two_manifests(csv_manifests):
    prev = manifest_utils.read_manifest(csv_manifests[4])
    curr = manifest_utils.read_manifest(csv_manifests[5])
    comparison = manifest_utils.join_manifests(prev, curr)
    assert len(comparison) == 5
    assert comparison["a.txt"] == ["abc123", "abc123"]
    assert comparison["b.txt"] == ["def456", None]
    assert comparison["c.txt"] == ["ghi789", None]
    assert comparison["d.txt"] == [None, "def456"]
    assert comparison["e.txt"] == [None, "jkl101"]


def test_join_three_manifests(csv_manifests):
    manifests = []
    manifests.append(manifest_utils.read_manifest(csv_manifests[4]))
    manifests.append(manifest_utils.read_manifest(csv_manifests[5]))
    manifests.append(manifest_utils.read_manifest(csv_manifests[6]))
    comparison = manifest_utils.join_manifests(*manifests)
    assert len(comparison) == 5
    assert comparison["a.txt"] == ["abc123", "abc123", None]
    assert comparison["b.txt"] == ["def456", None, "def456"]
    assert comparison["c.txt"] == ["ghi789", None, None]
    assert comparison["d.txt"] == [None, "def456", "mno112"]
    assert comparison["e.txt"] == [None, "jkl101", "jkl101"]


def test_compare_add(csv_manifests, capsys):
    paths = csv_manifests
    compare_manifests.compare_manifests(paths[1], paths[0])
    out = capsys.readouterr().out
    expected_out = [
            "b.txt: added",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_compare_delete(csv_manifests, capsys):
    paths = csv_manifests
    compare_manifests.compare_manifests(paths[0], paths[1])
    out = capsys.readouterr().out
    expected_out = [
            "b.txt: deleted",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_compare_change(csv_manifests, capsys):
    paths = csv_manifests
    compare_manifests.compare_manifests(paths[2], paths[0])
    out = capsys.readouterr().out
    expected_out = [
            "a.txt: changed",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_compare_rename(csv_manifests, capsys):
    paths = csv_manifests
    compare_manifests.compare_manifests(paths[3], paths[0])
    out = capsys.readouterr().out
    expected_out = [
            "a.txt: renamed to b.txt",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_compare_rename_of_existing(csv_manifests, capsys):
    paths = csv_manifests
    compare_manifests.compare_manifests(paths[3], paths[1])
    out = capsys.readouterr().out
    expected_out = [
            "a.txt: renamed to b.txt",
            "b.txt: changed",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_compare_rename_delete_add(csv_manifests, capsys):
    paths = csv_manifests
    compare_manifests.compare_manifests(paths[5], paths[4])
    out = capsys.readouterr().out
    expected_out = [
            "b.txt: renamed to d.txt",
            "c.txt: deleted",
            "e.txt: added",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_compare_delete_add_change(csv_manifests, capsys):
    '''
    This is technically the same as
    "d.txt: renamed to b.txt" and "d.txt was added",
    but I think that output is more confusing
    (Was d.txt added, then renamed? Or vice versa?) than
    "b.txt: added" and "d.txt changed"
    '''
    paths = csv_manifests
    compare_manifests.compare_manifests(paths[6], paths[5])
    out = capsys.readouterr().out
    expected_out = [
            "a.txt: deleted",
            "b.txt: added",
            "d.txt: changed",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_get_manifest_paths(csv_manifests, tmp_path):
    manifest_paths = manifest_utils.get_manifest_paths(tmp_path.as_posix())
    assert csv_manifests == manifest_paths


def test_file_history_a(csv_manifests, tmp_path, capsys):
    file_history.main("a.txt", tmp_path.as_posix())
    out = capsys.readouterr().out
    expected_out = [
            "a.txt: added in 0000000000",
            "a.txt: changed in 0000000002",
            "a.txt: deleted in 0000000003",
            "a.txt: added in 0000000004",
            "a.txt: deleted in 0000000006",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_file_history_b(csv_manifests, tmp_path, capsys):
    file_history.main("b.txt", tmp_path.as_posix())
    out = capsys.readouterr().out
    expected_out = [
            "b.txt: added in 0000000001",
            "b.txt: renamed to a.txt in 0000000002",
            "b.txt: added in 0000000003",
            "b.txt: changed in 0000000004",
            "b.txt: renamed to d.txt in 0000000005",
            "b.txt: added in 0000000006",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_file_history_c(csv_manifests, tmp_path, capsys):
    file_history.main("c.txt", tmp_path.as_posix())
    out = capsys.readouterr().out
    expected_out = [
            "c.txt: added in 0000000004",
            "c.txt: deleted in 0000000005",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_file_history_d(csv_manifests, tmp_path, capsys):
    file_history.main("d.txt", tmp_path.as_posix())
    out = capsys.readouterr().out
    expected_out = [
            "d.txt: added in 0000000005",
            "d.txt: changed in 0000000006",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_file_history_e(csv_manifests, tmp_path, capsys):
    file_history.main("e.txt", tmp_path.as_posix())
    out = capsys.readouterr().out
    expected_out = [
            "e.txt: added in 0000000005",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_file_history_f(csv_manifests, tmp_path, capsys):
    file_history.main("f.txt", tmp_path.as_posix())
    out = capsys.readouterr().out
    expected_out = [
            "File f.txt not found",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_duplicate_one_file(text_files, capsys):
    finddup.main(text_files[0])
    out = capsys.readouterr().out
    expected_out = [
            "duplicates:",
            "\ta.txt",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_duplicate_missing_file(capsys):
    filename = "does_not_exist"
    finddup.main(filename)
    out = capsys.readouterr().out
    expected_out = [
            ""  # pytest doesn't capture log output in the same way
            ]
    assert out == "\n".join(expected_out)


def test_duplicate_two_files_no_duplicate(text_files, capsys):
    finddup.main(text_files[0], text_files[1])
    out = capsys.readouterr().out
    expected_out = [
            "duplicates:",
            "\ta.txt",
            "duplicates:",
            "\tb.txt",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_duplicate_two_files_all_duplicate(text_files, capsys):
    finddup.main(text_files[0], text_files[2])
    out = capsys.readouterr().out
    expected_out = [
            "duplicates:",
            "\ta.txt",
            "\tc.txt",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_duplicate_three_files_two_groups(text_files, capsys):
    finddup.main(text_files[0], text_files[1], text_files[2])
    out = capsys.readouterr().out
    expected_out = [
            "duplicates:",
            "\ta.txt",
            "\tc.txt",
            "duplicates:",
            "\tb.txt",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_duplicate_three_files_two_groups_reordered(text_files, capsys):
    finddup.main(text_files[1], text_files[2], text_files[0])
    out = capsys.readouterr().out
    expected_out = [
            "duplicates:",
            "\ta.txt",
            "\tc.txt",
            "duplicates:",
            "\tb.txt",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_duplicate_four_files_two_unequal_groups(text_files, capsys):
    finddup.main(text_files[0], text_files[1], text_files[2], text_files[3])
    out = capsys.readouterr().out
    expected_out = [
            "duplicates:",
            "\ta.txt",
            "\tc.txt",
            "\td.txt",
            "duplicates:",
            "\tb.txt",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_duplicate_four_files_two_equal_groups(text_files, capsys):
    finddup.main(text_files[0], text_files[1], text_files[2], text_files[4])
    out = capsys.readouterr().out
    expected_out = [
            "duplicates:",
            "\ta.txt",
            "\tc.txt",
            "duplicates:",
            "\tb.txt",
            "\te.txt",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)


def test_duplicate_all_files(text_files, capsys):
    finddup.main(*text_files)
    out = capsys.readouterr().out
    expected_out = [
            "duplicates:",
            "\ta.txt",
            "\tc.txt",
            "\td.txt",
            "duplicates:",
            "\tb.txt",
            "\te.txt",
            "duplicates:",
            "\tf.txt",
            "\tg.txt",
            ""  # prints have extra newline
            ]
    assert out == "\n".join(expected_out)
