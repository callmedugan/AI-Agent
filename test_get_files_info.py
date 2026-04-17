from functions.get_files_info import *


print("Result for current directory:\n" + get_files_info("calculator", "."))
print('get_files_info("calculator", "pkg")' + get_files_info("calculator", "pkg"))
print('get_files_info("calculator", "/bin")' + get_files_info("calculator", "/bin"))
print('get_files_info("calculator", "../")' + get_files_info("calculator", "../"))