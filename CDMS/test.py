import string
import re
from datetime import datetime
# from validation import validateUser

letters = string.ascii_lowercase + string.ascii_uppercase

print(set(string.punctuation))

# while True:
#     word = input('naam: ')

#     if any(word.startswith(x) for x in letters):
#         print('zit in alfabet')
#     else:
#         print('nee niet')
# def validatePassword():
#     while True:
#         pattern = ("^(?=.*[a-z])(?=." +
#                 "*[A-Z])(?=.*\\d)" +
#                 "(?=.*[-+_!@#$%^&*., ?]).+$")
        
#         while True:  
#             password = input("password = : ")
#             if(len(password) <= 8 or len(password) > 30):
#                 print('Username MUST be between 8 and 30 characters')
#             else: 
#                 break
#         while True:
#             p = re.compile(pattern)
#             if(re.search(p, password)):
#                 return password
#             else:
#                 print('Must have at least 1 special characters, lowercase letter, uppercase letter and digit')
#                 break
    


# print(validatePassword())

print(datetime.now())