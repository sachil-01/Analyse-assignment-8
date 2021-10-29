import string
import re
from datetime import datetime
# from validation import validateUser

letters = string.ascii_lowercase + string.ascii_uppercase

# print(set(string.punctuation))

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

# print(datetime.day())
  
  
# def validateEmail():
#         pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
#         while True:
#             eMail = input('Please enter email address: ')
            
#             if(re.fullmatch(pattern, eMail)):
#                 print("Email set to " + eMail)
#                 return eMail
    
#             else:
#                 print("Invalid Email")


# validateEmail()

# def encrypt(string):
#     key = 5
#     message = ''
#     for letter in string:
#         new_letter = ord(letter) + key
#         message += chr(new_letter)
#     return message

# def decrypt(string):
#     key = 5
#     message = ''
#     for letter in string:
#         new_letter = ord(letter) - key
#         message += chr(new_letter)
#     return message


# print(decrypt('MFQQTT%INY%NX%JJS%YJXY'))
# print(encrypt("test"))

