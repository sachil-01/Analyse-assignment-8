import re
import string
import sqlite3
from datetime import datetime
import zipfile
import os


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
                print('Username MUST be between 8 and 30 characters')
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
        while True:
            try:
                while True:
                    try:
                        show_all_clients(self)
                        client = int(input('Please enter the client ID: '))
                        if(isinstance(client, int)):
                            break
                    except Exception as e:
                        print('Wrong input. Please enter a number')
                self.cur.execute("SELECT * FROM client WHERE person_id = ?", (client,))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('Client not found')
                else:
                    fetch = self.cur.execute("SELECT * FROM client WHERE person_id = ?", (client,))
                    test = fetch.fetchall()
                    fullname = test[0][1] # First element in first tuple in list
                    return [client,decrypt(fullname)]
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
        while True:
            try:
                advisor = 1
                user_name = encrypt(input('Please enter advisor username: ').lower())
                self.cur.execute("SELECT * FROM users WHERE lower(username) = ? AND advisor = ?", (user_name, advisor))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('Advisor not found ')
                else:
                    print('user found\n')
                    return user_name
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

def searchSysAdmin(self):
        while True:
            try:
                sys_admin = 1
                user_name = encrypt(input('Please enter system admin username: ').lower())
                self.cur.execute("SELECT * FROM users WHERE lower(username) = ? AND system_admin = ?", (user_name, sys_admin))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('system admin not found.')
                else:
                    print('user found\n')
                    return user_name
            except Exception as e:
                print(e)


def changeFullname(self, client,username, date_time):

    newName = input('Please enter new fullname for client: ')
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET fullname = ? WHERE person_id = ?", (encrypt(newName), client[0]))
        self.conn.commit()
        print('Fullname updated successfully')
        logActivity(self,username,date_time,'Fullname updated', 'Client name: ' + client[1] ,'No','No')

    except Exception as e:
            print(e)

    return

def changeAddress(self, client,username, date_time):

    newAddress = input('Please enter new address for client: ')
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET address = ? WHERE lower(fullname) = ?", (encrypt(newAddress), client[0]))
        self.conn.commit()
        print('Address updated successfully')
        logActivity(self,username,date_time,'address updated', 'Client name: ' + client[1] ,'No','No')

    except Exception as e:
            print(e)

    return

def changeZip(self, client, username, date_time):

    newZip = validateZip()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET zipcode = ? WHERE lower(fullname) = ?", (encrypt(newZip), client[0]))
        self.conn.commit()
        print('Zipcode updated successfully')
        logActivity(self,username,date_time,'Zipcode updated', 'Client name: ' + decrypt(client[1]) ,'No','No')

    except Exception as e:
            print(e)

    return


    


def changeCity(self, client, username, date_time):

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
            self.cur.execute("UPDATE client SET city = ? WHERE lower(fullname) = ?", (encrypt(city), client[0]))
            self.conn.commit()
            print('City updated successfully')
            logActivity(self,username,date_time,'City updated', 'Client name: ' + decrypt(client[1]) ,'No','No')

        except Exception as e:
                print(e)

        return



def changeEmail(self, client, username, date_time):
    
    email = validateEmail()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET email = ? WHERE lower(fullname) = ?", (encrypt(email), client[0]))
        self.conn.commit()
        print('email updated successfully')
        logActivity(self,username,date_time,'Email updated', 'Client name: ' + client[1] ,'No','No')

    except Exception as e:
            print(e)

    return


def changePhone(self, client, username, date_time):
    newPhone = validatePhone()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET phone_number = ? WHERE lower(fullname) = ?", (encrypt(newPhone), client[0]))
        self.conn.commit()
        print('phone number updated successfully')
        logActivity(self,username,date_time,'Phone number updated', 'Client name: ' + decrypt(client[1]) ,'No','No')

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
                else:
                    break
            while True:
                lastname = input('enter lastname: ')
                if(lastname == ""):
                    print('lastname cannot be empty! ')
                else:
                    break
            isAdvisor = 1
            isAdmin = 0
            isSysadmin = 0

        elif(number=='2'):
            while True:
                firstname = input('enter firstname: ')
                if(firstname == ""):
                    print('firstname cannot be empty! ')
                else:
                    break
            while True:
                lastname = input('enter lastname: ')
                if(lastname == ""):
                    print('lastname cannot be empty! ')
                else:
                    break
            isAdvisor = 0
            isAdmin = 0
            isSysadmin = 1
        else:
            firstname = input('enter firstname [OPTIONAL]:  ')
            lastname = input('enter lastname: [OPTIONAL]: ')
            isAdvisor = 0
            isAdmin = 1
            isSysadmin = 0
        timestamp = datetime.now()

        testlist = [user_name,passw,firstname,lastname]
        notEncrypted = [isAdmin,isSysadmin,isAdvisor,timestamp]
        EncryptedData = [encrypt(i) for i in testlist]

        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        try:
            self.cur.execute("INSERT INTO users(username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES (?,?,?,?,?,?,?,?)", EncryptedData + notEncrypted)
            self.conn.commit()
            print('User sucessfully added.')

            logActivity(self, username, date_time, 'new ' + 'Admin created' if isAdmin == 1 else ('Advisor created' if isAdvisor == 1 else 'System admin created') ,'username is ' + user_name, 'No', 'No')

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
    newName = input('firstname: ')
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
    newLastName = input('Lastname: ')
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
        admin = searchAdmin(self).lower()
        try:
            self.cur.execute("DELETE FROM users WHERE lower(username) = ?", (admin, ))
            self.conn.commit()
            print('User successfully Deleted.')
            logActivity(self,username,date_time,'Admin deleted', 'username: '+ decrypt(admin),'No','No')

        except Exception as e:
            print(e)
        return
    elif(number=='2'):
        sys_admin = searchSysAdmin(self).lower()
        try:
            self.cur.execute("DELETE FROM users WHERE lower(username) = ?", (sys_admin, ))
            self.conn.commit()
            print('User successfully Deleted.')
            logActivity(self,username,date_time,'System admin deleted', 'username: '+ decrypt(sys_admin),'No','No')

        except Exception as e:
            print(e)
        return



def deleteAdvisor(self, username, date_time):
    user_name = searchAdvisor(self)
    try:
        self.cur.execute("DELETE FROM users WHERE username = ?", (user_name, ))
        self.conn.commit()
        print('User sucessfully Deleted.')
        logActivity(self,username,date_time,'Advisor  deleted', 'username: '+ decrypt(user_name),'No','No')

    except Exception as e:
        print(e)
    return

def zip_files(self,username,date_time):
    list_files = ['DB_backup.sql']
        
    try:
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
    key = 5
    message = ''
    for letter in string:
        new_letter = ord(letter) + key
        message += chr(new_letter)
    return message

def decrypt(string):
    key = 5
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
        print('Client ' + str(row[0]) + ' = ' + decrypt(row[1]))
        clientCount += 1


def show_all_users(self):
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    userCount = 1
    print('---List of Users---')
    for row in self.cur.execute('SELECT * FROM users ORDER BY admin, system_admin, advisor'):
        if(row[4] == 1):
            print('User ' + str(userCount) + ' = ' + decrypt(row[0]) + ' | Role: superadmin')
        elif(row[5]== 1):
            print('User ' + str(userCount) + ' = ' + decrypt(row[0]) + ' | Role: system admin')
        else:
            print('User ' + str(userCount) + ' = ' + decrypt(row[0]) + ' | Role: advisor')
        userCount += 1
