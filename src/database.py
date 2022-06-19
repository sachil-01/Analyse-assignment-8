import sqlite3
import io
from ui import *
from termcolor import colored
from validation import *
from datetime import datetime
import os
import random

# GLobal Variables

# --------------------------------------------------------------------
max_input_try = 3
company_db_name = 'mycompany.db'
client_tb_name = 'client'
users_tb_name = 'users'
user_type = ""
username = ""
now = datetime.now()  # current date and time
date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
notification = False
message = ''
loginAttempt = 1


# User
# --------------------------------------------------------------------
class user:
    def __init__(self, user_data):
        self.username = user_data[0]
        self.password = user_data[1]
        self.firstname = user_data[2]
        self.lastname = user_data[3]
        self.admin = user_data[4]

# Database
# --------------------------------------------------------------------


class db:
    global db_menu, username

    def __init__(self, db_name, client_table_name, users_table_name):
        self.db_name = db_name
        self.client_table_name = client_table_name
        self.users_table_name = users_table_name

        self.loggedin = 0
        self.loggedin_user = None
        self.admin_is_loggedin = 0

        self.reset()

    def reset(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

        # create client table if it does not exist
        tb_create = "CREATE TABLE client (client_id CHAR, firstname CHAR, lastname CHAR, address TEXT, zipcode TEXT, city TEXT, email TEXT, phone_number TEXT, joinDate TIMESTAMP)"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            self.cur.execute(
                "INSERT INTO client (client_id ,firstname, lastname, address, zipcode, city, email, phone_number, joinDate) VALUES ('96676<;869', 'Pmpm', 'Erhivwsr', 'fekmnrlsj$58', '7555OE', 'Wglmiheq', 'xiwxDkqemp2gsq', ';;6<7=<6', '2021-10-25 18:09:12.091144' )")
            # self.cur.execute("INSERT INTO client (fullname, address, zipcode, city, email, phone_number) VALUES ('Anne Banwarth', 'bagijnhof 14', '3111KA', 'Schiedam', 'test@gmail.com', '0677283982')")
            self.conn.commit()
        except Exception as e:
            print(e)

        # create user table if it does not exist
        tb_create = "CREATE TABLE users (username TEXT, password TEXT, firstname TEXT, lastname TEXT, admin INT, system_admin INT, advisor INT, joinDate TIMESTAMP);"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            self.cur.execute(
                "INSERT INTO users (username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES ('wytivehqmr', 'Ehqmr765%', 'firns', '', 5, 4, 4,'2021-10-25 18:09:12.091144')")
            self.cur.execute(
                "INSERT INTO users (username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES ('xiwx', 'xiwx' , '', '', 5, 4, 4,'2021-10-25 18:09:12.091144')")
            self.cur.execute(
                "INSERT INTO users (username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES ('w}wehqmr', 'Ehqmr%67' , '', '', 4, 5, 4,'2021-10-25 18:09:12.091144')")
            self.cur.execute(
                "INSERT INTO users (username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES ('ehzmwsv', 'Ehqmr%67' , '', '', 4, 4, 5,'2021-10-25 18:09:12.091144')")
            self.conn.commit()
        except Exception as e:
            print(e)

        # create logging table if it does not exist
        tb_create = "CREATE TABLE logging (username TEXT, date TEXT, description TEXT, additional_information TEXT, suspicious TEXT, read TEXT);"
        try:
            self.cur.execute(tb_create)
            self.conn.commit()
        except Exception as e:
            print(e)

    def login(self):
        global user_type, username, db_menu, loginAttempt
        username = input("please enter username: ").lower()
        password = input("please enter password: ")

        # string concatenation
        # sql_statement = f"SELECT * from users WHERE username='{username}' AND password='{password}'"
        # sql_statement = f'SELECT * from users WHERE username="{username}" AND password="{password}"'

        # PREPARED STATEMENT 1 (qmark style)
        sql_statement = (
            "SELECT * from users WHERE username = ? AND password = ?", (username, password))
        # Prepared statement 2 (named style)
        # self.cur.execute("SELECT * from users WHERE username=:username AND password=:password",
        # {"username": username, "password": password})

        try:
            self.cur.execute("SELECT * from users WHERE lower(username) = ? AND password = ?",
                             (encrypt(username), encrypt(password)))

        except OperationalError as ErrorMessage:
            print("Invalid input")
            logActivity(self, username, date_time,
                        'Invalid input', '', 'Yes', 'No')

        loggedin_user = self.cur.fetchone()
        if not loggedin_user:  # An empty result evaluates to False.
            print("Invalid username or password.")
            if(loginAttempt == 3):
                print("Login failed for 3 attempts, exiting program")
                logActivity(self, username, date_time, 'Login blocked after 3 attempts',
                            'password: ' + password + ' is tried with with username: ' + username, "Yes", "No")
                quit()
            else:
                loginAttempt += 1
            logActivity(self, username, date_time, 'Unsuccessful login', 'password: ' +
                        password + ' is tried with with username: ' + username, "Yes", "No")
        else:
            logActivity(self, username, date_time, 'Logged in', '', 'No', 'No')
            self.loggedin = 1
            self.loggedin_user = username
            if(loggedin_user[4] == 5):
                user_type = 'Super Administrator'
                db_menu = admin_menu
            elif(loggedin_user[5] == 5):
                user_type = 'System Administrator'
                db_menu = sysadmin_menu
            else:
                user_type = 'Advisor'
                db_menu = advisor_menu

            notification = showNotification(self)
            message = ''

            print('\n\n\n\nWelcome')
            heading = '▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄' + '\n' + \
                      '▍ ' + '\n' + \
                      '▍ Username: ' + colored(self.loggedin_user, 'red') + '\n' + \
                      '▍ ' + '\n' + \
                      '▍ User type: ' + colored(user_type, 'red') + '\n' + \
                      '▍ ' + '\n' + \
                      '▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀' + '\n' + \
                      'User Menu'

            db_interface = user_interface(
                user_type, message, notification, heading, db_menu)
            db_interface.run()
            del db_interface

    def show_all_clients(self):

        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

        clientCount = 1
        print('---List of Clients---')
        for row in self.cur.execute('SELECT * FROM client'):
            print('Client ' + str(clientCount) + ' = ' + decrypt(row[1]))
            clientCount += 1

    def show_all_users(self):
        # self.not_implemented(self.show_all_users)
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

        userCount = 1
        print('---List of Users---')
        for row in self.cur.execute('SELECT * FROM users ORDER BY admin, system_admin, advisor'):
            if(row[4] == 5):
                print('User ' + str(userCount) + ' = ' +
                      decrypt(row[0]) + ' | Role: Super Administrator')
            elif(row[5] == 5):
                print('User ' + str(userCount) + ' = ' +
                      decrypt(row[0]) + ' | Role: System Administrator')
            else:
                print('User ' + str(userCount) + ' = ' +
                      decrypt(row[0]) + ' | Role: Advisor')
            userCount += 1

    def add_new_client(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        while True:
            firstname = input('Please enter firstname: ')
            if(firstname == ""):
                print('fullname cannot be empty')
            else:
                break
        print('firstname = ' + firstname)
        while True:
            lastname = input('Please enter lastname: ')
            if(lastname == ""):
                print('lastname cannot be empty')
            else:
                break
        print('lastname = ' + lastname)
        fullName = firstname + ' ' + lastname

        address = input('Please enter address: ')
        print('address = ' + address)
        zipcode = validateZip()
        print('zipcode = ' + zipcode)

        CityNames = [[1, 'Den haag'], [2, 'Rotterdam'], [3, 'Schiedam'], [4, 'Arnhem'], [5, 'Amsterdam'], [6, 'Nijmegen'], [7, 'Haarlem'],
                     [8, 'Delft'], [9, 'Eindhoven'], [10, 'Breda']]

        while True:
            for i in CityNames:
                print(str(i[0]) + ' = ' + str(i[1]))

            print('')
            chosenNumber = input('Please choose a city from 1-10: ')
            if (chosenNumber not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']):
                print('Invalid number\n')
            else:
                break
        city = CityNames[int(chosenNumber)-1][1]
        print('City = ' + str(city))
        eMail = validateEmail()

        phoneNumber = validatePhone()
        print('Phone number is ' + str(phoneNumber))
        timestamp = datetime.now()
        joinDate = timestamp.strftime("%d-%m-%Y, %H:%M:%S")
        client_id = generate_string_id()
        while True:
            self.cur.execute(
                "SELECT * FROM client WHERE client_id = ?", ((encrypt(client_id)),))
            data = self.cur.fetchall()
            if(len(data) == 0):
                break
            client_id = generate_string_id()
        print("generating new id")
        entry = [client_id, firstname, lastname, address,
                 zipcode, city, eMail, phoneNumber, joinDate]

        EncryptedData = [encrypt(i) for i in entry]

        try:
            self.cur.execute(
                "INSERT INTO client(client_id, firstname, lastname, address, zipcode, city, email, phone_number, joinDate) VALUES (?,?,?,?,?,?,?,?,?)", EncryptedData)
            self.conn.commit()
            print('Client sucessfully added.')
            logActivity(self, username, date_time, 'New client created',
                        'Client name: ' + fullName, 'No', 'No')

        except Exception as e:
            print(e)

    def add_new_user(self):
        while True:
            if(user_type == 'Super Administrator'):
                print('[1] advisor\n[2] system admin\n')
                print('Which user do you want to make?')
                number = input()
                if(number in ['1', '2']):
                    add_new_users(self, number, username, date_time)
                    return
                else:
                    print('Enter a valid number.')

            elif(user_type == 'System Administrator'):
                print('[1] advisor\n')
                print('Which user do you want to make?')
                number = input()
                if(number in ['1']):
                    add_new_users(self, '1', username, date_time)
                    return
                else:
                    print('Enter a valid number.\n')

    def delete_client_record(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT * FROM client')
        data = self.cur.fetchall()
        if len(data) == 0:
            print('No clients in the system')
            return
        clientCount = 1
        print('---List of Clients---')
        for row in self.cur.execute('SELECT * FROM client'):
            print('Client ' + str(clientCount) + ' = ' +
                  decrypt(row[1]) + " " + decrypt(row[2]))
            clientCount += 1

        clientNumber = 0
        while True:
            try:
                SelectedClientNumber = input("Please enter client number : ")
                if(isinstance(int(SelectedClientNumber), int) and int(SelectedClientNumber) >= 1 and int(SelectedClientNumber) <= len(data)):
                    clientNumber = int(SelectedClientNumber)
                    break
                else:
                    print(f"Enter a number between 1 - {len(data)} ")
            except Exception as e:
                print(f"Enter a number between 1 - {len(data)} ")
            # return data[clientNumber-1][0]

        print(f'___Client number {clientNumber}___\n')
        print('client_id = ' + decrypt(data[clientNumber-1][0]))
        print('firstname = ' + decrypt(data[clientNumber-1][1]))
        print('lastname = ' + decrypt(data[clientNumber-1][2]))
        print('address = ' + decrypt(data[clientNumber-1][3]))
        print('zipcode = ' + decrypt(data[clientNumber-1][4]))
        print('city = ' + decrypt(data[clientNumber-1][5]))
        print('email = ' + decrypt(data[clientNumber-1][6]))
        print('phone number = ' + decrypt(data[clientNumber-1][7]))
        print('\n')

        print("\n")
        print('[1] firstname\n[2] lastname\n[3] address\n[4] zipcode\n[5] city\n[6] email\n[7] phone number\n')
        print('Which record do you want to delete? Please choose 1-7')

        empty = ""
        while True:
            record = input('number: ')
            if(record in ['1', '2', '3', '4', '5', '6', '7']):
                break
            else:
                print('Please enter a valid number')
        if(record == '1'):
            try:
                self.cur.execute(
                    "UPDATE client SET firstname = ? WHERE client_id = ?", (empty, data[clientNumber-1][0]))
                self.conn.commit()
                print('firstname record has been deleted.')
                logActivity(self, username, date_time, 'firstname deleted',
                            'Client name: ' + decrypt(data[clientNumber-1][1]), 'No', 'No')

            except Exception as e:
                print(e)
            return
        elif(record == '2'):
            try:
                self.cur.execute(
                    "UPDATE client SET lastname = ? WHERE client_id = ?", (empty, data[clientNumber-1][0]))
                self.conn.commit()
                print('lastname record has been deleted.')
                logActivity(self, username, date_time, 'lastname deleted',
                            'Client name: ' + decrypt(data[clientNumber-1][1]), 'No', 'No')
            except Exception as e:
                print(e)
            return
        elif(record == '3'):
            try:
                self.cur.execute(
                    "UPDATE client SET address = ? WHERE client_id = ?", (empty, data[clientNumber-1][0]))
                self.conn.commit()
                print('address record has been deleted.')
                logActivity(self, username, date_time, 'Address deleted',
                            'Client name: ' + decrypt(data[clientNumber-1][1]), 'No', 'No')
            except Exception as e:
                print(e)
            return
        elif(record == '4'):
            try:
                self.cur.execute(
                    "UPDATE client SET zipcode = ? WHERE client_id = ?", (empty, data[clientNumber-1][0]))
                self.conn.commit()
                print('zipcode record has been deleted.')
                logActivity(self, username, date_time, 'Zipcode deleted',
                            'Client name: ' + decrypt(data[clientNumber-1][1]), 'No', 'No')
            except Exception as e:
                print(e)
            return
        elif(record == '5'):
            try:
                self.cur.execute(
                    "UPDATE client SET city = ? WHERE  client_id = ?", (empty, data[clientNumber-1][0]))
                self.conn.commit()
                print('city record has been deleted.')
                logActivity(self, username, date_time, 'City deleted',
                            'Client name: ' + decrypt(data[clientNumber-1][1]), 'No', 'No')
            except Exception as e:
                print(e)
        elif(record == '6'):
            try:
                self.cur.execute(
                    "UPDATE client SET email = ? WHERE client_id = ?", (empty, data[clientNumber-1][0]))
                self.conn.commit()
                print('email record has been deleted.')
                logActivity(self, username, date_time, 'Email deleted',
                            'Client name: ' + decrypt(data[clientNumber-1][1]), 'No', 'No')
            except Exception as e:
                print(e)
            return
        else:
            try:
                self.cur.execute(
                    "UPDATE client SET phone_number = ? WHERE client_id = ?", (empty, data[clientNumber-1][0]))
                self.conn.commit()
                print('phone number record has been deleted.')
                logActivity(self, username, date_time, 'Phone number deleted',
                            'Client name: ' + decrypt(data[clientNumber-1][1]), 'No', 'No')
            except Exception as e:
                print(e)
            return

    def deleteAdvisor(self):
        user_name = searchAdvisor(self)
        try:
            self.cur.execute(
                "DELETE FROM users WHERE lower(username) = ?", (user_name, ))
            self.conn.commit()
            print('User sucessfully Deleted.')

        except Exception as e:
            print(e)
        return

    def make_a_user_admin(self):
        # self.not_implemented(self.make_a_user_admin)
        print('---This user will be set to admin---\n')
        user = searchUser(self)

        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()

        try:
            self.cur.execute(
                "UPDATE users SET admin = ?, system_admin = ?, advisor = ? WHERE lower(username) = ?", (1, 0, 0, user))
            self.conn.commit()
            print('New admin set succesfully')
            logActivity(self, username, date_time, 'User updated to admin',
                        'user ' + decrypt(user) + ' updated to admin', 'No', 'No')

        except Exception as e:
            print(e)
        return

    def delete_client(self):
        try:
            while True:
                while True:
                    self.conn = sqlite3.connect(self.db_name)
                    self.cur = self.conn.cursor()
                    self.cur.execute("SELECT * FROM client")
                    data = self.cur.fetchall()
                    if(len(data) == 0):
                        print("No clients in system")
                        return
                    search = encrypt(
                        input('Please enter keywords to search: '))
                    break
                self.conn = sqlite3.connect(self.db_name)
                self.cur = self.conn.cursor()
                counter = 1
                self.cur.execute("SELECT * FROM client WHERE client_id LIKE ? OR firstname LIKE ? OR lastname LIKE ? OR address LIKE ? OR email LIKE ? OR phone_number LIKE ?",
                                 ('%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%'))
                data = self.cur.fetchall()
                if(len(data) == 0):
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
                counter += 1
            clientNumber = 0
            while True:
                try:
                    SelectedClientNumber = input(
                        "Please enter client number : ")
                    if(isinstance(int(SelectedClientNumber), int) and int(SelectedClientNumber) >= 1 and int(SelectedClientNumber) <= len(data)):
                        clientNumber = int(SelectedClientNumber)
                        break
                    else:
                        print(f"Enter a number between 1 - {len(data)} ")
                except Exception as e:
                    print(f"Enter a number between 1 - {len(data)} ")
            client = data[clientNumber-1][0]
            self.cur.execute(
                "DELETE FROM client WHERE client_id = ?", (client, ))
            self.conn.commit()
            print('Client successfully Deleted.')
            logActivity(self, username, date_time, 'Client deleted',
                        'username: ' + decrypt(data[clientNumber-1][1]), 'No', 'No')

        except Exception as e:
            print(e)

    def delete_user(self):
        while True:
            if(user_type == 'Super Administrator'):
                print('Which user do you want to delete?')
                print('[1] system admin\n[2] advisor\n')
                number = input('Number: ')
                if(number not in ['1', '2']):
                    print('Please enter a number between 1-2')
                else:
                    break

        if(number == '1'):
            deleteUsers(self, number, username, date_time)
            return
        else:
            deleteAdvisor(self, username, date_time)
            return

    def change_password(self):
        # self.not_implemented(self.change_password)
        print('Please enter new password')
        newPass = validatePassword()

        try:
            self.cur.execute("UPDATE users SET password = ? WHERE username = ?", (encrypt(
                newPass), encrypt(username)))
            self.conn.commit()
            print('Password updated successfully')
            logActivity(self, username, date_time,
                        'Changed own password', '', 'No', 'No')

        except Exception as e:
            print(e)

    def update_client_info(self):
        while True:
            self.conn = sqlite3.connect(self.db_name)
            self.cur = self.conn.cursor()
            self.cur.execute("SELECT * FROM client")
            data = self.cur.fetchall()
            if len(data) == 0:
                print('No clients in the system')
                return
            search = encrypt(input('Please enter keywords to search: '))
            self.cur.execute("SELECT * FROM client")
            data = self.cur.fetchall()
            if len(data) == 0:
                print('No clients in the system')
                return
            counter = 1
            self.cur.execute("SELECT * FROM client WHERE client_id LIKE ? OR firstname LIKE ? OR lastname LIKE ? OR address LIKE ? OR email LIKE ? OR phone_number LIKE ?",
                             ('%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%'))
            data = self.cur.fetchall()
            if(len(data) == 0):
                print("No entries found, try again.")
            else:
                break
        for entry in data:
            print(f'___Client number {counter}___\n')
            print('client_id = ' + decrypt(entry[0]))
            print('firstname = ' + decrypt(entry[1]))
            print('lastname = ' + decrypt(entry[2]))
            print('address = ' + decrypt(entry[3]))
            print('zipcode = ' + decrypt(entry[4]))
            print('city = ' + decrypt(entry[5]))
            print('email = ' + decrypt(entry[6]))
            print('phone number = ' + decrypt(entry[7]))
            print('\n')
            counter += 1

        numbers = [int(i) for i in range(len(data))]

        clientNumber = 0
        while True:
            try:
                SelectedClientNumber = input(
                    "Please enter Client number to update: ")
                if(isinstance(int(SelectedClientNumber), int) and int(SelectedClientNumber) >= 1 and int(SelectedClientNumber) <= len(data)):
                    clientNumber = int(SelectedClientNumber)
                    break
                else:
                    print(f"Enter a number between 1 - {len(data)} ")
            except Exception as e:
                print(f"Enter a number between 1 - {len(data)} ")

        # if(SelectedClientNumber>=1 and SelectedClientNumber < len(data)):
        # SelectClient = data[SelectedClientNumber-1]
        print(f"Client {clientNumber} has been selected.\n")
        print('client_id = ' + decrypt(data[clientNumber-1][0]))
        print('firstname = ' + decrypt(data[clientNumber-1][1]))
        print('lastname = ' + decrypt(data[clientNumber-1][2]))
        print('address = ' + decrypt(data[clientNumber-1][3]))
        print('zipcode = ' + decrypt(data[clientNumber-1][4]))
        print('city = ' + decrypt(data[clientNumber-1][5]))
        print('email = ' + decrypt(data[clientNumber-1][6]))
        print('phone number = ' + decrypt(data[clientNumber-1][7]))
        print('\n')
        columns = ['firstname', 'lastname', 'address',
                   'zipcode', 'city', 'email', 'phone number']
        count = 1
        try:
            for i in columns:
                print('[' + str(count) + '] ' + i)
                count += 1
        except Exception as e:
            print(e)
        print('')
        while True:
            chosenNumber = input(
                'Please enter which info you want to update 1-7: ')
            if(chosenNumber in ['1', '2', '3', '4', '5', '6', '7']):
                break
            else:
                print('Please enter a valid number')
        client_id = [data[clientNumber-1][0], data[clientNumber-1][1]]
        if(chosenNumber == '1'):
            changeFirstnameClient(self, client_id, username, date_time)
        elif(chosenNumber == '2'):
            changeLastnameClient(self, client_id, username, date_time)
        elif(chosenNumber == '3'):
            changeAddress(self, client_id, username, date_time)
        elif(chosenNumber == '4'):
            changeZip(self, client_id, username, date_time)
        elif(chosenNumber == '5'):
            changeCity(self, client_id, username, date_time)
        elif(chosenNumber == '6'):
            changeEmail(self, client_id, username, date_time)
        else:
            changePhone(self, client_id, username, date_time)

    def get_client_info(self):
        client = searchClientnew(self)
        return

    def reset_advisor_password(self):

        advisor_name = searchAdvisor(self)
        if(advisor_name == "no entries found in the database"):
            return
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        temp_psw = 'Welkom@01'

        print("Advisor password will be set to temporary password Welkom@01")

        try:
            self.cur.execute("UPDATE users SET password = ? WHERE lower(username) = ?", (encrypt(
                temp_psw), advisor_name))
            self.conn.commit()
            print('password updated successfully')
            logActivity(self, username, date_time, 'Advisor password reset',
                        'username: ' + decrypt(advisor_name), 'No', 'No')

        except Exception as e:
            print(e)
        return

    def reset_admin_password(self):

        admin_name = searchSysAdmin(self)
        if(admin_name == "no entries found in the database"):
            return
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        temp_psw = 'P@ssw0rd100'

        print("Admin password will be set to temporary password: P@ssw0rd100")

        try:
            self.cur.execute("UPDATE users SET password = ? WHERE lower(username) = ?", (encrypt(
                temp_psw), admin_name))
            self.conn.commit()
            print('password updated successfully')
            logActivity(self, username, date_time, 'Admin password reset',
                        'username: ' + decrypt(admin_name), 'No', 'No')

        except Exception as e:
            print(e)
        return

    def update_advisor_info(self):

        print('Which advisor do you want to update?')
        name = searchAdvisor(self)

        columns = ['username', 'password', 'firstname', 'lastname']

        count = 1
        try:
            for i in columns:
                print('[' + str(count) + '] ' + i)
                count += 1
        except Exception as e:
            print(e)
        print('')
        while True:
            chosenNumber = input(
                'Please enter which info you want to update 1-4: ')
            if(chosenNumber in ['1', '2', '3', '4']):
                break
            else:
                print('Please enter a valid number')

        if(chosenNumber == '1'):
            changeUsername(self, name, username, date_time)
        elif(chosenNumber == '2'):
            changePassword(self, name, username, date_time)
        elif(chosenNumber == '3'):
            changeFirstname(self, name, username, date_time)
        else:
            changeLastname(self, name, username, date_time)

    def update_systemadmin_info(self):

        print('Which system admin do you want to update?')
        name = searchSysAdmin(self)
        if(name == "no entries found in the database"):
            return

        columns = ['username', 'password', 'firstname', 'lastname']

        count = 1
        try:
            for i in columns:
                print('[' + str(count) + '] ' + i)
                count += 1
        except Exception as e:
            print(e)
        print('')
        while True:
            chosenNumber = input(
                'Please enter which info you want to update 1-4: ')
            if(chosenNumber in ['1', '2', '3', '4']):
                break
            else:
                print('Please enter a valid number')

        if(chosenNumber == '1'):
            changeUsername(self, name, username, date_time)
        elif(chosenNumber == '2'):
            changePassword(self, name, username, date_time)
        elif(chosenNumber == '3'):
            changeFirstname(self, name, username, date_time)
        else:
            changeLastname(self, name, username, date_time)

    def create_db_backup(self):
        self.conn = sqlite3.connect(self.db_name)
        try:

            with io.open('DB_backup.sql', 'w', encoding='utf-8') as p:

                for line in self.conn.iterdump():

                    p.write('%s\n' % line)

            print(' Backup has been created!')
            print(' Data Saved as DB_backup.sql')
            zip_files(self, username, date_time)
            self.conn.close()
            logActivity(self, username, date_time, 'Database backup created',
                        'DB_backup.sql created and zipped', 'No', 'No')
        except Exception as e:
            print(e)

    def restore_backup(self):
        try:
            path_to_file = "backup.zip"
            cwd = os.getcwd()

            if(os.path.exists(path_to_file)):
                with zipfile.ZipFile(path_to_file, 'r') as zip_ref:
                    zip_ref.extractall(cwd)

                self.conn = sqlite3.connect(self.db_name)
                self.cur.execute("DROP TABLE client")
                self.cur.execute("DROP TABLE logging")
                self.cur.execute("DROP TABLE users")
                f = open('DB_backup.sql', 'r',
                         encoding='cp932', errors='ignore')
                sql = f.read()
                self.cur.executescript(sql)
                f.close()
                if(os.path.exists('DB_backup.sql')):
                    os.remove('DB_backup.sql')
                print("Backup has been restored")
            else:
                print("No backup has been made")
                return
        except Exception as e:
            print(e)

    def showLogs(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("SELECT * FROM logging")
            data = self.cur.fetchall()
            decryptedData = [(decrypt(tuple[0]), decrypt(tuple[1]), decrypt(tuple[2]), decrypt(
                tuple[3]), decrypt(tuple[4]), decrypt(tuple[5])) for tuple in data]
            header = ("username", "date", "description",
                      "additional information", "suspicious", "read")
            widths = [len(cell) for cell in header]
            for row in data:
                for i, cell in enumerate(row):
                    widths[i] = max(len(str(cell)), widths[i])

            formatted_row = ' '.join('{:%d}' % width for width in widths)

            print(formatted_row.format(*header))
            for row in decryptedData:
                print(formatted_row.format(*row))
            readActivity(self)

        except Exception as e:
            print(e)

    def logout(self):
        self.loggedin = 0
        self.loggedin_user = None
        self.admin_is_loggedin = 0

    def close(self):
        self.conn.close()

    def not_implemented(self, func):
        print(func.__name__ + ' method is Not implemented')


def escape_sql_meta(sql_query):
    pass


client = db(company_db_name, client_tb_name, users_tb_name)
main_menu = [[1, 'login', client.login], [0, 'Exit', client.close]]
admin_menu = [[1, 'show all clients', client.show_all_clients], [2, 'show all users', client.show_all_users],
              [3, 'add new client', client.add_new_client], [
                  4, 'add new user', client.add_new_user],
              [5, 'delete a user', client.delete_user],
              [6, 'delete a client', client.delete_client], [
                  7, 'delete client record', client.delete_client_record],
              [8, 'change password', client.change_password], [9, 'reset advisor password', client.reset_advisor_password], [
                  10, 'reset system admin password', client.reset_admin_password], [11, 'update client info', client.update_client_info],
              [12, 'update advisor info', client.update_advisor_info], [13, 'update system admin info', client.update_systemadmin_info], [
                  14, 'search client info', client.get_client_info], [15, 'backup database', client.create_db_backup],
              [16, 'restore database', client.restore_backup], [17, 'show logs', client.showLogs], [0, 'logout', client.logout]]


advisor_menu = [[1, 'show all clients', client.show_all_clients], [2, 'change password', client.change_password],
                [3, 'add new client', client.add_new_client], [
                    4, 'search client info', client.get_client_info],
                [5, 'update client info', client.update_client_info], [0, 'logout', client.logout]]

sysadmin_menu = [[1, 'show all clients', client.show_all_clients], [2, 'show all users', client.show_all_users], [3, 'change password', client.change_password],
                 [4, 'add new client', client.add_new_client], [5, 'add new advisor',
                                                                client.add_new_user], [6, 'search client info', client.get_client_info],
                 [7, 'update client info', client.update_client_info], [8, 'update advisor info',
                                                                        client.update_advisor_info], [9, 'reset advisor password', client.reset_advisor_password],
                 [10, 'delete a client', client.delete_client], [11, 'delete a advisor', client.deleteAdvisor], [
                     12, 'delete client record', client.delete_client_record], [13, 'backup database', client.create_db_backup],
                 [14, 'restore database', client.restore_backup], [15, 'Show logs', client.showLogs], [0, 'logout', client.logout]]
