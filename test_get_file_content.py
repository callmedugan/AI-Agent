from functions.get_file_content import *

print("Result for file content in lorem.txt:\n" + get_file_content("calculator", "lorem.txt"))
print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
print(get_file_content("calculator", "/bin/cat")) #(this should return an error string)
print(get_file_content("calculator", "pkg/does_not_exist.py")) #(this should return an error string))