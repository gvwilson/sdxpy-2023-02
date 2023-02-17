def sign(value):
    if value < 0:
        return -1
    else:
        return 1
    
def test_sign_negative():
    assert sign(-3) == -1
test_sign_negative.skip = True

def test_sign_positive():
    assert sign(19) == 1

def test_sign_zero():
    assert sign(0) == 0
test_sign_zero.fail = True

def test_sign_error():
    assert sgn(1) == 1

def classify(func):
    if hasattr(func, "skip") and func.skip:
        return "skip"
    if hasattr(func, "fail") and func.fail:
        return "fail"
    return "run"

def find_tests(prefix):
    for (name, func) in globals().items():
        if name.startswith(prefix):
            print(name, func)

def run_tests(prefix):
    results = {}
    all_names = [n for n in globals() if n.startswith(prefix)]
    for name in all_names:
        func = globals()[name]
        kind = classify(func)
        try:
            if kind == "skip":
                results[name] = 'skip'
            else:
                func()
                results[name] = 'pass'
        except AssertionError as e:
            if kind == "fail":
                results[name] = 'pass'
            else: 
                results[name] = 'fail'
        except Exception as e:
            results[name] = 'error - ' + str(e)
    print('fail: '+ str(len([x for x in results.values() if x=='fail']))+'\n'
                             + 'pass: ' + str(len([x for x in results.values() if x == 'pass']))+'\n'
                             + 'error: ' + str(len([x for x in results.values() if x.startswith('error')]))+'\n'
                             + 'skip: ' + str(len([x for x in results.values() if x == 'skip']))
             )
    for (name, result) in results.items() :
        print(f"{result}: {name}")
    return results

def check_run_tests():
    results = run_tests("test_")
    assert all([results['test_sign_negative'] == 'skip',
            results['test_sign_positive'] == 'pass',
            results['test_sign_zero'] == 'pass',
            results['test_sign_error'].startswith('error')]
            )

run_tests('check_')
