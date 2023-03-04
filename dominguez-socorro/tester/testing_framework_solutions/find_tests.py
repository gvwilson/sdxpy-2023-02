# Function to modify for Wednesday's class
from glob import glob
from importlib.machinery import SourceFileLoader


def find_tests():
    results = {"pass": [], "fail": [], "error": []}
    test_files = glob("**/test_*.py", recursive=True)
    
    for (i, name) in enumerate(test_files):
        m = SourceFileLoader(f"m{i}", name).load_module()

        for name in dir(m):
            if not name.startswith("test_"):
                continue
            func = getattr(m, name)
            try:
                func()
                results["pass"].append(func.__name__)
            except AssertionError:
                results["fail"].append(func.__name__)
            except Exception:
                results["error"].append(func.__name__)
                
    results['summary'] = {'pass': len(results['pass']),
                          'fail': len(results['fail']),
                          'error': len(results['error'])}
                              
    return results



# Failing on Purpose Q3
def find_tests_assert():
    results = {"pass": [], "fail": [], "error": []}
    test_files = glob("**/test_*.py", recursive=True)
    
    for (i, name) in enumerate(test_files):
        m = SourceFileLoader(f"m{i}", name).load_module()

        for name in dir(m):
            if not name.startswith("test_"):
                continue
            func = getattr(m, name)
            
            if (func.__doc__ == "test:assert"): 
                try:
                    func()
                except AssertionError:
                    results["pass"].append(func.__name__)
                else:
                    results["fail"].append(func.__name__)
                
            else:    
                try:
                    func()
                    results["pass"].append(func.__name__)
                except AssertionError:
                    results["fail"].append(func.__name__)
                except Exception:
                    results["error"].append(func.__name__)
                
    results['summary'] = {'pass': len(results['pass']),
                          'fail': len(results['fail']),
                          'error': len(results['error'])}
                              
    return results


# Setup & Teardown Q4
def find_tests_st():
    results = {"pass": [], "fail": [], "error": []}
    test_files = glob("**/test_*.py", recursive=True)
    
    for (i, name) in enumerate(test_files):
        m = SourceFileLoader(f"m{i}", name).load_module()

        for name in dir(m):
            if not name.startswith("test_"):
                continue
            func = getattr(m, name)
            
            if "setup" in globals():
                setup()
            
            if (func.__doc__ == "test:assert"): 
                try:
                    func()
                except AssertionError:
                    results["pass"].append(func.__name__)
                else:
                    results["fail"].append(func.__name__)
                
            else:    
                try:
                    func()
                    results["pass"].append(func.__name__)
                except AssertionError:
                    results["fail"].append(func.__name__)
                except Exception:
                    results["error"].append(func.__name__)
            
            if "teardown" in globals():
                teardown()
                
    results['summary'] = {'pass': len(results['pass']),
                          'fail': len(results['fail']),
                          'error': len(results['error'])}
                              
    return results