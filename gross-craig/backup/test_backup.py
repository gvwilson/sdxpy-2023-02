import pytest
import csv
import compare_manifests


@pytest.fixture()
def csv_manifests(tmp_path):
    """Save three sample manifest csv to the tmp_path directory

    Parameters
    ----------
    tmp_path : temporary directory fixture from pytest

    Returns
    -------
    list of paths

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
    yield list(manifests.keys())
    for path in manifests.keys():
        path.unlink()


def test_read_manifests(csv_manifests):
    manifest_dict = compare_manifests.read_manifest(csv_manifests[4])
    assert len(manifest_dict.keys()) == 3
    assert "a.txt" in manifest_dict.keys()
    assert manifest_dict["a.txt"] == "abc123"
    assert "b.txt" in manifest_dict.keys()
    assert manifest_dict["b.txt"] == "def456"
    assert "c.txt" in manifest_dict.keys()
    assert manifest_dict["c.txt"] == "ghi789"


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
