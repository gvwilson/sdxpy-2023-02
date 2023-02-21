from glob import glob
from importlib.machinery import SourceFileLoader

result_groups = {
    'pass': [],
    'fail': [],
    'skip': [],
    'error': [],
}


def render_result_groups(result_groups):
    print()
    print('=== Test results ===')

    for (ttype, tests) in result_groups.items():
        for test in tests:
            print(f'{test} {ttype}')

    print('Totals:')
    for (ttype, tests) in result_groups.items():
        print(f'{len(tests)} {ttype}')


def run_tests(finder):
    test_files = finder

    result_groups_temp = result_groups.copy()

    for (i, name) in enumerate(test_files):
        m = SourceFileLoader(f"m{i}", name).load_module()

        names = dir(m)
        setup_func, teardown_func = None, None
        if 'setup' in names:
            setup_func = getattr(m, 'setup')
        if 'teardown' in names:
            teardown_func = getattr(m, 'teardown')


        for name in names:
            if not name.startswith("test_"):
                continue
            func = getattr(m, name)
            if setup_func:
                setup_func()
            try:
                func()
                result_type = 'pass'
            except AssertionError:
                if func.__doc__ == 'test:assert':
                    result_type = 'pass'
                else:
                    result_type = 'fail'
            except Exception:
                result_type = 'error'

            if teardown_func:
                teardown_func()

            result_groups_temp[result_type].append(func.__name__)

    return result_groups_temp


def run_tests_stats_meta_test():
    finder = glob("test_testsuite_stats.py", root_dir=".", recursive=False)
    res = run_tests(finder)
    assert res == {'pass': ['test_stats_test1', 'test_stats_test2'],
                   'fail': ['test_stats_test3'],
                   'skip': [],
                   'error': ['test_stats_test4']
                   }
    print("run_tests_stats_meta_test ran successfully")


def run_all_test_stats():
    finder = glob("**/test_*.py", root_dir=".", recursive=True)
    res = run_tests(finder)
    rendered_res = render_result_groups(res)
    print(rendered_res)


run_all_test_stats()
# run_tests_stats_meta_test()
