from .. import compare_manifests


def test_compare_manifests():
    want = [
        'changed: file-with-changed-content.txt',
        'renamed: file-with-original-name.txt -> file-with-changed-name.txt',
        'created: file-that-gets-added.txt',
        'created: another-file-that-gets-added.txt',
        'deleted: file-that-gets-deleted.txt',
        'deleted: another-file-that-gets-deleted.txt',
    ]
    got = compare_manifests('manifests/manifest-2023-01-01.csv',
                            'manifests/manifest-2023-01-02.csv')
    assert want == got
