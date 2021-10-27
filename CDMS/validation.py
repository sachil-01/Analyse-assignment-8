import re
import string
import sqlite3
from datetime import datetime


# make a pattern


def validateUser():
    pattern = "^[A-Za-z0-9_'.-]*$"
    while True:
        while True:  
            # input
            username = input("username = : ")
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
                client = input('Please enter full name of client: ')
                self.cur.execute("SELECT * FROM client WHERE fullname = ?", (client,))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('There is no client named %s'%client)
                else:
                    print('client found\n')
                    for row in self.cur.execute("SELECT fullname, address, zipcode, city, email, phone_number FROM client WHERE fullname = ?", (client,)):
                        print(row)
                        return client
                    break
            except Exception as e:
                print(e)

def searchUser(self):
        while True:
            try:
                user_name = input('Please enter username : ')
                self.cur.execute("SELECT * FROM users WHERE username = ?", (user_name,))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('There is no user named %s'%user_name)
                else:
                    print('user found\n')
                    return user_name
            except Exception as e:
                print(e)

def searchAdvisor(self):
        while True:
            try:
                advisor = 1
                user_name = input('Please enter advisor username: ')
                self.cur.execute("SELECT * FROM users WHERE username = ? AND advisor = ?", (user_name, advisor))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('There is no advisor named %s'%user_name)
                else:
                    print('user found\n')
                    return user_name
            except Exception as e:
                print(e)

def searchAdmin(self):
        while True:
            try:
                admin = 1
                user_name = input('Please enter admins username: ')
                self.cur.execute("SELECT * FROM users WHERE username = ? AND admin = ?", (user_name, admin))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('There is no admin named %s'%user_name)
                else:
                    print('user found\n')
                    return user_name
            except Exception as e:
                print(e)

def searchSysAdmin(self):
        while True:
            try:
                sys_admin = 1
                user_name = input('Please enter system admin username: ')
                self.cur.execute("SELECT * FROM users WHERE username = ? AND system_admin = ?", (user_name, sys_admin))
                data=self.cur.fetchall()
                if len(data)==0:
                    print('There is no system admin named %s'%user_name)
                else:
                    print('user found\n')
                    return user_name
            except Exception as e:
                print(e)


def changeFullname(self, client):

    newName = input('Please enter new fullname for client: ')
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET fullname = ? WHERE fullname = ?", (newName, client))
        self.conn.commit()
        print('Fullname updated successfully')

    except Exception as e:
            print(e)

    return

def changeAddress(self, client):

    newAddress = input('Please enter new address for client: ')
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET address = ? WHERE fullname = ?", (newAddress, client))
        self.conn.commit()
        print('Address updated successfully')

    except Exception as e:
            print(e)

    return

def changeZip(self, client):

    newZip = validateZip()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET zipcode = ? WHERE fullname = ?", (newZip, client))
        self.conn.commit()
        print('Zipcode updated successfully')

    except Exception as e:
            print(e)

    return


    


def changeCity(self, client):

        CityNames = [[1,'Den haag'], [2,'Rotterdam'], [3,'Schiedam'], [4,'Arnhem'], [5,'Amsterdam'],[6,'Nijmegen'], [7,'Haarlem'],
                    [8,'Delft'],[9,'Eindhoven'], [10,'Breda']]

        while True:
            for i in CityNames:
                print(str(i[0]) + ' = ' + str(i[1]))

            print('')
            chosenNumber = input('Please choose a city from 1-10: ')
            if int(chosenNumber) not in [1,2,3,4,5,6,7,8,9,10]:
                print('Invalid number\n')
            else:
                break
        city = CityNames[int(chosenNumber)-1][1]

        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        try:
            self.cur.execute("UPDATE client SET city = ? WHERE fullname = ?", (city, client))
            self.conn.commit()
            print('City updated successfully')

        except Exception as e:
                print(e)

        return



def changeEmail(self, client):
    
    email = validateEmail()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET email = ? WHERE fullname = ?", (email, client))
        self.conn.commit()
        print('email updated successfully')

    except Exception as e:
            print(e)

    return


def changePhone(self, client):
    newPhone = validatePhone()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE client SET phone_number = ? WHERE fullname = ?", (newPhone, client))
        self.conn.commit()
        print('phone number updated successfully')

    except Exception as e:
            print(e)

    return

def changeUsername(self, advisor_name):
    
    print('Please enter a new username for ' + advisor_name)
    user_name = validateUser()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE users SET username = ? WHERE username = ?", (user_name, advisor_name))
        self.conn.commit()
        print('Username updated successfully')

    except Exception as e:
            print(e)

    return

def add_new_users(self,number):
        user_name = validateUser()
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

        testtuple = (user_name,passw,firstname,lastname,isAdmin,isSysadmin,isAdvisor,timestamp)

        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        try:
            self.cur.execute("INSERT INTO users(username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES (?,?,?,?,?,?,?,?)", testtuple)
            self.conn.commit()
            print('User sucessfully added.')

        except Exception as e:
            print(e)
        return


def changePassword(self, advisor_name):
    print('Please enter a new password for ' + advisor_name)
    new_pass = validatePassword()
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()

    try:
        self.cur.execute("UPDATE users SET password = ? WHERE username = ?", (new_pass, advisor_name))
        self.conn.commit()
        print('Password updated successfully')

    except Exception as e:
            print(e)
    return

def changeFirstname(self, advisor_name):
    print('Enter a new firstname for '+ advisor_name)
    newName = input('firstname: ')
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()
    try:
        self.cur.execute("UPDATE users SET firstname = ? WHERE username = ?", (newName, advisor_name))
        self.conn.commit()
        print('Firstname updated successfully')

    except Exception as e:
            print(e)
    return

def changeLastname(self, advisor_name):
    print('Enter a new lastname for '+ advisor_name)
    newLastName = input('Lastname: ')
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()
    try:
        self.cur.execute("UPDATE users SET lastname = ? WHERE username = ?", (newLastName, advisor_name))
        self.conn.commit()
        print('Lastname updated successfully')

    except Exception as e:
            print(e)
    return

def deleteUsers(self, number):
    self.conn = sqlite3.connect(self.db_name) 
    self.cur = self.conn.cursor()
    if(number=='1'):
        admin = searchAdmin(self)
        try:
            self.cur.execute("DELETE FROM users WHERE username = ?", (admin, ))
            self.conn.commit()
            print('User sucessfully Deleted.')

        except Exception as e:
            print(e)
        return
    elif(number=='2'):
        sys_admin= searchSysAdmin(self)
        try:
            self.cur.execute("DELETE FROM users WHERE username = ?", (sys_admin, ))
            self.conn.commit()
            print('User sucessfully Deleted.')

        except Exception as e:
            print(e)
        return



def deleteAdvisor(self):
    user_name = searchAdvisor(self)
    try:
        self.cur.execute("DELETE FROM users WHERE username = ?", (user_name, ))
        self.conn.commit()
        print('User sucessfully Deleted.')

    except Exception as e:
        print(e)
    return





# while True:
#     firstname = input("firstname = : ")

#     pattern = re.compile("[A-Za-z0-9]+")
#     pattern.fullmatch(firstname)

#         # if found match (entire string matches pattern)
#     if pattern.fullmatch(firstname) is not None:
#         print("Found match: " + firstname)
#     else:
#         # if not found match
#         print("No match")