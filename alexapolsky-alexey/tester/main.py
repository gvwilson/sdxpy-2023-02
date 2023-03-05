

try:
    for name in globals():
        print(name)

except RuntimeError as e:
    assert str(e) == 'dictionary changed size during iteration'


name = None
for name in globals():
    print(name)

