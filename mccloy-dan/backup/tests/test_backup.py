from .. import compare_manifests, file_history, parse_entry


def test_compare_manifests():
    want = [
        'changed: file-with-changed-content.txt',
        'renamed: file-with-original-name.txt -> file-with-changed-name.txt',
        'created: file-that-gets-added.txt',
        'created: another-file-that-gets-added.txt',
        'deleted: file-that-gets-deleted.txt',
        'deleted: another-file-that-gets-deleted.txt',
    ]
    output = compare_manifests('manifests/manifest-2023-01-01.csv',
                               'manifests/manifest-2023-01-02.csv')
    got = [entry[key] for entry in output for key in entry]
    assert want == got


def test_file_history():
    want = [
        '2023-01-04: created',
        '2023-01-06: changed',
        '2023-01-07: deleted',
    ]
    output = file_history('b.txt')
    got = [f"{timestamp}: {event.split(':')[0]}"
           for timestamp, _, event in
           map(parse_entry, output)]
    assert want == got
    # these should match because they're renamings of each other:
    assert file_history('a.txt') == file_history('aaa.txt')
