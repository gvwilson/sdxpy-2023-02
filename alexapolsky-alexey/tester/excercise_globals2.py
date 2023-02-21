

name = None
for name in globals():
    print(name)

print("EOF reached successfully, we are at the end of script")
print("I am still figuring out why in this case dict has not changed dynamically, I understand that assignment did "
      "the trick, but what specifically it did under the hood? or is it just a convention/conditional, which if meets"
      "None in the target variable name in ast.For(), it simply doesn't create a dict entry as agreed")


