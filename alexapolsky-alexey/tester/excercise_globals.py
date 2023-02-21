

try:
    for name in globals():
        print(name)

except RuntimeError as e:
    assert str(e) == 'dictionary changed size during iteration'
    print("As expected, the iteration is adding a target variable into the global scope, so exception is raised\n"
          "because globals uses dynamic view() object that is monitoring changes and errors out on iteration")



