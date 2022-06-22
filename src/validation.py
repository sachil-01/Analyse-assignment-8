from itertools import count
import re
import string
import sqlite3
from datetime import datetime
import zipfile
import os
import os.path
import random


# make a pattern

def checkUserExist(self):
        while True:
            try:
                username = encrypt(input('Enter username: ').lower())
                self.cur.execute("SELECT lower(username) FROM users WHERE lower(username) = ?", (username,))
                exists = self.cur.fetchall()
                if exists:
                    print("Username already chosen...")
                else:
                    return decrypt(username)
            except Exception as e:
                print(e)   
        
                return

def validateUser(self):
    pattern = "^[A-Za-z0-9_'.-]*$"
    while True:
        while True:  
            # input
            username = checkUserExist(self)
            if(len(username) < 5 or len(username) > 20):
                print('Username MUST be between 5 and 20 characters')
            else: 
                break
        while True:
            alfabet = string.ascii_lowercase + string.ascii_uppercase
            if any(username.startswith(x) for x in alfabet):
                state = bool(re.match(pattern, username))
                if(state):
                    return username
                else:
                    print('Wrong format')
                    break
            else:
                print('Make sure you begin with a letter')
                break
                


def validateZip():
    while True:
        pattern = "^[0-9]{4}[A-Z]{2}$"

        zipcode = input("Please Enter zipcode in format (DDDDXX) with capital letters: ")
        state = bool(re.match(pattern, zipcode))
        if(state):
            return zipcode
        print('Zipcode Invalid')


def validatePhone():
    while True:
        print('Please enter an 8 digit phone number in format (+31-6-DDDDDDDD)')
        number = input("Please enter 8 digit number: ")
        
        if re.match(pattern="^\d{8}$", string=number):
             return "+31-6-"+number
        else: 
            print("wrong phone number")

def validatePassword():
    while True:
        pattern = ("^(?=.*[a-z])(?=." +
                "*[A-Z])(?=.*\\d)" +
                "(?=.*[-+_!@#$%^&*., ?]).+$")
        
        while True:  
            password = input("password = : ")
            if(len(password) < 8 or len(password) > 30):
                print('Password MUST be between 8 and 30 characters')
            else: 
                break
        while True:
            p = re.compile(pattern)
            if(re.search(p, password)):
                return password
            else:
                print('Must have at least 1 special characters, lowercase letter, uppercase letter and digit')
                break

def validateEmail():
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        while True:
            eMail = input('Please enter email address: ')
            
            if(re.fullmatch(pattern, eMail)):
                print("Email set to " + eMail)
                return eMail
    
            else:
                print("Invalid Email")
        
        

def searchClient(self):
        # while True:
        #     try:
        #         while True:
        #             try:
                        show_all_clients(self)
                        return
                        # client = int(input('Please enter the client ID: '))
            #             if(isinstance(client, int)):
            #                 break
            #         except Exception as e:
            #             print('Wrong input. Please enter a number')
            #     self.cur.execute("SELECT * FROM client WHERE person_id = ?", (client,))
            #     data=self.cur.fetchall()
            #     if len(data)==0:
            #         print('Client not found')
            #     else:
            #         fetch = self.cur.execute("SELECT * FROM client WHERE person_id = ?", (client,))
            #         test = fetch.fetchall()
            #         fullname = test[0][1] # First element in first tuple in list
            #         return [client,decrypt(fullname)]
            # except Exception as e:
            #     print(e)

def searchClientnew(self):
    try:
        while True:
            while True:
                self.conn = sqlite3.connect(self.db_name) 
                self.cur = self.conn.cursor()
                self.cur.execute("SELECT * FROM client")
                data=self.cur.fetchall()
                if len(data)==0:
                    print('No clients in the system')
                    return
                search = encrypt(input('Please enter keywords to search: '))
                break
            counter = 1
            self.cur.execute("SELECT * FROM client WHERE client_id LIKE ? OR firstname LIKE ? OR lastname LIKE ? OR address LIKE ? OR email LIKE ? OR phone_number LIKE ?", ('%'+search+'%','%'+search+'%','%'+search+'%','%'+search+'%','%'+search+'%','%'+search+'%'))
            data = self.cur.fetchall()
            if(len(data)==0):
                print("No entries found, try again.")
            else:
                break
        for entry in data:
            print(f'___Client {counter}___\n')
            print('client_id = ' + decrypt(entry[0]))
            print('firstname = ' + decrypt(entry[1]))
            print('lastname = ' + decrypt(entry[2]))
            print('address = ' + decrypt(entry[3]))
            print('zipcode = ' + decrypt(entry[4]))
            print('city = ' + decrypt(entry[5]))
            print('email = ' + decrypt(entry[6]))
            print('phone number = ' + decrypt(entry[7]))
            print('\n')
            counter+=1
    except Exception as e: 
        print(e)
        

def searchUser(self):
        while True:
            try:
                show_all_users(self)
                user_name = encrypt(input('Please enter username : ').lower())
                self.cur.execute("SELECT * FROM users WHERE lower(username) = ?", (user_name,))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('User not found')
                else:
                    return user_name
            except Exception as e:
                print(e)

def searchAdvisor(self):
            try:
                while True:
                    while True:
                        self.conn = sqlite3.connect(self.db_name) 
                        self.cur = self.conn.cursor()
                        self.cur.execute("SELECT * FROM users WHERE advisor = 5")
                        data = self.cur.fetchall()
                        if(len(data)==0):
                            print("No advisors in system")
                            return "no entries found in the database"
                        search = encrypt(input('Please enter keywords to search: '))
                        break
                    self.conn = sqlite3.connect(self.db_name) 
                    self.cur = self.conn.cursor()
                    counter = 1
                    self.cur.execute("SELECT * FROM users WHERE advisor = 5")
                    data = self.cur.fetchall()
                    if(len(data)==0):
                        print("No advisors in system")
                        return
                    self.cur.execute("SELECT * FROM users WHERE advisor = 5 AND (username LIKE ? OR firstname LIKE ? OR lastname LIKE ?)", ('%'+search+'%','%'+search+'%','%'+search+'%'))
                    data = self.cur.fetchall()
                    if(len(data)==0):
                        print("No entries found, try again.")
                    else:
                        break
                for entry in data:
                    print(f'___Advisor number {counter}___\n')
                    print('username = ' + decrypt(entry[0]))
                    print('firstname = ' + decrypt(entry[2]))
                    print('lastname = ' + decrypt(entry[3]))
                    print('\n')
                    counter+=1
                clientNumber = 0
                while True:
                    try:
                        SelectedClientNumber = input("Please enter advisor number : ")
                        if(isinstance(int(SelectedClientNumber), int) and int(SelectedClientNumber) >= 1 and int(SelectedClientNumber) <= len(data)):
                            clientNumber = int(SelectedClientNumber)
                            break
                        else:
                            print(f"Enter a number between 1 - {len(data)} ")
                    except Exception as e:
                        print(f"Enter a number between 1 - {len(data)} ")
                return data[clientNumber-1][0]
            except Exception as e:
                print(e)

def searchSysAdmin(self):
            try:
                while True:
                    while True:
                        self.conn = sqlite3.connect(self.db_name) 
                        self.cur = self.conn.cursor()
                        self.cur.execute("SELECT * FROM users WHERE system_admin = 5")
                        data = self.cur.fetchall()
                        if(len(data)==0):
                            print("No system administrator in system")
                            return "no entries found in the database"
                        search = encrypt(input('Please enter keywords to search: '))
                        break
                    self.conn = sqlite3.connect(self.db_name) 
                    self.cur = self.conn.cursor()
                    counter = 1
                    self.cur.execute("SELECT * FROM users WHERE system_admin = 5 AND (username LIKE ? OR firstname LIKE ? OR lastname LIKE ?)", ('%'+search+'%','%'+search+'%','%'+search+'%'))
                    data = self.cur.fetchall()
                    if(len(data)==0):
                        print("No entries found, try again.")
                    else:
                        break
                for entry in data:
                    print(f'___System administrator number {counter}___\n')
                    print('username = ' + decrypt(entry[0]))
                    print('firstname = ' + decrypt(entry[2]))
                    print('lastname = ' + decrypt(entry[3]))
                    print('\n')
                    counter+=1
                clientNumber = 0
                while True:
                    try:
                        SelectedClientNumber = input("Please enter system administrator number : ")
                        if(isinstance(int(SelectedClientNumber), int) and int(SelectedClientNumber) >= 1 and int(SelectedClientNumber) <= len(data)):
                            clientNumber = int(SelectedClientNumber)
                            break
                        else:
                            print(f"Enter a number between 1 - {len(data)} ")
                    except Exception as e:
                        print(f"Enter a number between 1 - {len(data)} ")
                return data[clientNumber-1][0]
            except Exception as e:
                print(e)

def searchAdmin(self):
        while True:
            try:
                admin = 1
                user_name = encrypt(input('Please enter admins username: ').lower())
                self.cur.execute("SELECT * FROM users WHERE lower(username) = ? AND admin = ?", (user_name, admin))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('Admin not found')
                else:
                    print('user found\n')
                    return user_name
            except Exception as e:
                print(e)

# def searchSysAdmin(self):
#         while True:
#             try:
#                 sys_admin = 1
#                 user_name = encrypt(input('Please enter system admin username: ').lower())
#                 self.cur.execute("SELECT * FROM users WHERE lower(username) = ? AND system_admin = ?", (user_name, sys_admin))
#                 data=self.cur.fetchall()
#                 if len(data)==0:
#                     print('system admin not found.')
#                 else:
#                     print('user found\n')
#                     return user_name
#             except Exception as e:
#                 print(e)


def changeFirstnameClient(self, client_id,username, date_time):

    while True:
        newName = input('Please enter new firstname for client: ')
        if(newName == ""):
            print("firstname cannot be empty")
        elif(len(newName) > 20):
            print("firstname cannot be longer than 20 characters")
        else:
            break
    
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET firstname = ? WHERE client_id = ?", (encrypt(newName), client_id[0]))
        self.conn.commit()
        print('Firstname updated successfully')
        logActivity(self,username,date_time,'firstname updated', 'Client name: ' + decrypt(client_id[1]) ,'No','No')

    except Exception as e:
            print(e)

    return

def changeLastnameClient(self, client_id,username, date_time):

    while True:
        newName = input('Please enter new lastname for client: ')
        if(newName == ""):
            print("Lastname cannot be empty")
        elif(len(newName) > 20):
            print("Lastname cannot be longer than 20 characters")
        else:
            break
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET lastname = ? WHERE client_id = ?", (encrypt(newName), client_id[0]))
        self.conn.commit()
        print('Lastname updated successfully')
        logActivity(self,username,date_time,'lastname updated', 'Client name: ' + decrypt(client_id[1]) ,'No','No')

    except Exception as e:
            print(e)

    return

def changeAddress(self, client_id,username, date_time):

    while True:
        newAddress = input('Please enter new address for client: ')
        if(newAddress == ""):
            print("Address cannot be empty")
        elif(len(newAddress) > 30):
            print("Address cannot be longer than 30 characters")
        else:
            break
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET address = ? WHERE client_id = ?", (encrypt(newAddress), client_id[0]))
        self.conn.commit()
        print('Address updated successfully')
        logActivity(self,username,date_time,'address updated', 'Client name: ' + decrypt(client_id[1]) ,'No','No')

    except Exception as e:
            print(e)

    return

def changeZip(self, client_id, username, date_time):

    newZip = validateZip()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET zipcode = ? WHERE client_id = ?", (encrypt(newZip), client_id[0]))
        self.conn.commit()
        print('Zipcode updated successfully')
        logActivity(self,username,date_time,'Zipcode updated', 'Client name: ' + decrypt(client_id[1]) ,'No','No')

    except Exception as e:
            print(e)

    return


    


def changeCity(self, client_id, username, date_time):

        CityNames = [[1,'Den haag'], [2,'Rotterdam'], [3,'Schiedam'], [4,'Arnhem'], [5,'Amsterdam'],[6,'Nijmegen'], [7,'Haarlem'],
                    [8,'Delft'],[9,'Eindhoven'], [10,'Breda']]

        while True:
            for i in CityNames:
                print(str(i[0]) + ' = ' + str(i[1]))

            print('')
            chosenNumber = input('Please choose a city from 1-10: ')
            if (chosenNumber not in ['1','2','3','4','5','6','7','8','9','10']):
                print('Invalid number\n')
            else:
                break
        city = CityNames[int(chosenNumber)-1][1]

        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        try:
            self.cur.execute("UPDATE client SET city = ? WHERE client_id = ?", (encrypt(city), client_id[0]))
            self.conn.commit()
            print('City updated successfully')
            logActivity(self,username,date_time,'City updated', 'Client name: ' + decrypt(client_id[1]) ,'No','No')

        except Exception as e:
                print(e)

        return



def changeEmail(self, client_id, username, date_time):
    
    email = validateEmail()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET email = ? WHERE client_id = ?", (encrypt(email), client_id[0]))
        self.conn.commit()
        print('email updated successfully')
        logActivity(self,username,date_time,'Email updated', 'Client name: ' + decrypt(client_id[1]) ,'No','No')

    except Exception as e:
            print(e)

    return


def changePhone(self, client_id, username, date_time):
    newPhone = validatePhone()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET phone_number = ? WHERE client_id = ?", (encrypt(newPhone), client_id[0]))
        self.conn.commit()
        print('phone number updated successfully')
        logActivity(self,username,date_time,'Phone number updated', 'Client name: ' + decrypt(client_id[1]) ,'No','No')

    except Exception as e:
            print(e)

    return

def changeUsername(self, advisor_name, username, date_time):
    
    print('Please enter a new username: ')
    user_name = validateUser(self)
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE users SET username = ? WHERE lower(username) = ?", (encrypt(user_name), advisor_name))
        self.conn.commit()
        print('Username updated successfully')
        logActivity(self,username,date_time,'Username updated', 'username: ' + decrypt(advisor_name) + ' updated to ' + user_name ,'No','No')

    except Exception as e:
            print(e)

    return

def add_new_users(self,number, username, date_time):
        user_name = validateUser(self)
        passw = validatePassword()
        if(number =='1'):
            while True:
                firstname = input('enter firstname: ')
                if(firstname == ""):
                    print('firstname cannot be empty! ')
                elif(len(firstname) > 20):
                    print("firstname cannot be longer than 20 characters")
                else:
                    break
            while True:
                lastname = input('enter lastname: ')
                if(lastname == ""):
                    print('lastname cannot be empty! ')
                elif(len(lastname) > 20):
                    print("lastname cannot be longer than 20 characters")
                else:
                    break
            isAdvisor = 5
            isAdmin = 4
            isSysadmin = 4

        elif(number=='2'):
            while True:
                firstname = input('enter firstname: ')
                if(firstname == ""):
                    print('firstname cannot be empty! ')
                elif(len(firstname) > 20):
                    print("firstname cannot be longer than 20 characters")
                else:
                    break
            while True:
                lastname = input('enter lastname: ')
                if(lastname == ""):
                    print('lastname cannot be empty! ')
                elif(len(lastname) > 20):
                    print("lastname cannot be longer than 20 characters")
                else:
                    break
            isAdvisor = 4
            isAdmin = 4
            isSysadmin = 5
        timestamp = datetime.now()
        joinDate = timestamp.strftime("%d-%m-%Y, %H:%M:%S")

        testlist = [user_name,passw,firstname,lastname]
        notEncrypted = [isAdmin,isSysadmin,isAdvisor,encrypt(joinDate)]
        EncryptedData = [encrypt(i) for i in testlist]

        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        try:
            self.cur.execute("INSERT INTO users(username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES (?,?,?,?,?,?,?,?)", EncryptedData + notEncrypted)
            self.conn.commit()
            print('User sucessfully added.')

            logActivity(self, username, date_time, 'new ' + 'Admin created' if isAdmin == 5 else ('Advisor created' if isAdvisor == 5 else 'System admin created') ,'username is ' + user_name, 'No', 'No')

        except Exception as e:
            print(e)
        return


def changePassword(self, advisor_name, username, date_time):
    print('Please enter a new password:  ')
    new_pass = validatePassword()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE users SET password = ? WHERE lower(username) = ?", (encrypt(new_pass), advisor_name))
        self.conn.commit()
        print('Password updated successfully')
        logActivity(self,username,date_time,'Password updated', 'username: ' + decrypt(advisor_name) ,'No','No')

    except Exception as e:
            print(e)
    return

def changeFirstname(self, advisor_name, username, date_time):
    print('Enter a new firstname:  ')
    while True:
        newName = input('Please enter new firstname for client: ')
        if(newName == ""):
            print("firstname cannot be empty")
        elif(len(newName) > 20):
            print("firstname cannot be longer than 20 characters")
        else:
            break
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()
    try:
        self.cur.execute("UPDATE users SET firstname = ? WHERE lower(username) = ?", (encrypt(newName), advisor_name))
        self.conn.commit()
        print('Firstname updated successfully')
        logActivity(self,username,date_time,'Firstname updated', 'username: ' + decrypt(advisor_name) ,'No','No')

    except Exception as e:
            print(e)
    return

def changeLastname(self, advisor_name, username, date_time):
    print('Enter a new lastname: ')
    while True:
        newLastName = input('Please enter new lastname for client: ')
        if(newLastName == ""):
            print("lastname cannot be empty")
        elif(len(newLastName) > 20):
            print("lastname cannot be longer than 20 characters")
        else:
            break
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()
    try:
        self.cur.execute("UPDATE users SET lastname = ? WHERE lower(username) = ?", (encrypt(newLastName), advisor_name))
        self.conn.commit()
        print('Lastname updated successfully')
        logActivity(self,username,date_time,'Lastname updated', 'username: ' + decrypt(advisor_name) ,'No','No')

    except Exception as e:
            print(e)
    return

def deleteUsers(self, number, username, date_time):
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()
    if(number=='1'):
        admin = searchSysAdmin(self).lower()
        if(admin == "no entries found in the database"):
            return
        try:
            self.cur.execute("DELETE FROM users WHERE lower(username) = ?", (admin, ))
            self.conn.commit()
            print('User successfully Deleted.')
            logActivity(self,username,date_time,'Admin deleted', 'username: '+ decrypt(admin),'No','No')

        except Exception as e:
            print(e)
        return



def deleteAdvisor(self, username, date_time):
    user_name = searchAdvisor(self)
    if(user_name=="no entries found in the database"):
        return
    try:
        self.cur.execute("DELETE FROM users WHERE username = ?", (user_name, ))
        self.conn.commit()
        print('User sucessfully Deleted.')
        logActivity(self,username,date_time,'Advisor  deleted', 'username: '+ decrypt(user_name),'No','No')

    except Exception as e:
        print(e)
    return

# def deletesystemadmin(self, username, date_time):
#         user_name = searchsysadmin(self)
#         try:
#             self.cur.execute("DELETE FROM users WHERE username = ?", (user_name, ))
#             self.conn.commit()
#             print('User sucessfully Deleted.')
#             logActivity(self,username,date_time,'Advisor  deleted', 'username: '+ decrypt(user_name),'No','No')

#         except Exception as e:
#             print(e)
#         return

def zip_files(self,username,date_time):
    list_files = ['DB_backup.sql']
        
    try:
        if os.path.exists("backup.zip"):
            os.remove("backup.zip")

        with zipfile.ZipFile('backup.zip', 'w') as zipF:
            for file in list_files:
                zipF.write(file, compress_type=zipfile.ZIP_DEFLATED)

        print('File has been zipped')
        if os.path.exists("DB_backup.sql"):
            os.remove("DB_backup.sql")
        else:
            print("Nothing to remove")
        
    except Exception as e:
        print(e)



def encrypt(string):
    key = 4
    message = ''
    for letter in string:
        new_letter = ord(letter) + key
        message += chr(new_letter)
    return message

def decrypt(string):
    key = 4
    message = ''
    for letter in string:
        new_letter = ord(letter) - key
        message += chr(new_letter)
    return message


def logActivity(self, username, date, description, add_info, suspicious, read):
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()
    try:
        info = [username,date,description,add_info,suspicious, read]
        for i, v in enumerate(info):
            info[i] = encrypt(v)

        self.cur.execute("INSERT INTO logging(username, date, description, additional_information, suspicious, read) VALUES (?,?,?,?,?,?)", info)
        self.conn.commit()

    except Exception as e:
        print(e)
    return

def readActivity(self):
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE logging SET read = ? WHERE read = ? ", (encrypt("Yes"),encrypt("No"),))
        self.conn.commit()
        print('Log has been viewed')
        

    except Exception as e:
        print(e)

def showNotification(self):
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()
    
    try:
        sus = (encrypt('Yes'),encrypt('No'))
        self.cur.execute("SELECT * FROM logging WHERE suspicious = ? AND read = ?", (sus))
        data=self.cur.fetchall()
        if len(data)==0:
            return False
        else:
            return True
    except Exception as e:
                print(e)


def show_all_clients(self):

    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    clientCount = 1
    print('---List of Clients---')
    for row in self.cur.execute('SELECT * FROM client'):
        print('Client ' + str(clientCount) + ' = ' + decrypt(row[1]) + decrypt(row[2]))
        clientCount += 1


def show_all_users(self):
        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        userCount = 1
        print('---List of Users---')
        for row in self.cur.execute('SELECT * FROM users ORDER BY admin, system_admin, advisor'):
            if(row[4] == 5):
                print('User ' + str(userCount) + ' = ' + decrypt(row[0]) + ' | Role: Super Administrator')
            elif(row[5]== 5):
                print('User ' + str(userCount) + ' = ' + decrypt(row[0]) + ' | Role: System Administrator')
            else:
                print('User ' + str(userCount) + ' = ' + decrypt(row[0]) + ' | Role: Advisor')
            userCount += 1

def generate_string_id():
    #checken nog op dubbel
    x =random.randint(100000000,999999999)
    sum = 0
    for digit in str(x):
        sum += int(digit)
    remainder = sum % 10
    member_id = str(x) + str(remainder)
    return member_id