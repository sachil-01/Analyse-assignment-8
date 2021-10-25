import sqlite3
from ui import *
from termcolor import colored
from validation import *
from datetime import datetime

# GLobal Variables

# --------------------------------------------------------------------
max_input_try = 3
company_db_name = 'mycompany.db'
client_tb_name = 'client'
users_tb_name = 'users'
user_type = ""
username = ""


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
        tb_create = "CREATE TABLE client (person_id INTEGER PRIMARY KEY AUTOINCREMENT, fullname CHAR, address TEXT, zipcode TEXT, city TEXT, email TEXT, phone_number TEXT)"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            self.cur.execute("INSERT INTO client (fullname, address, zipcode, city, email, phone_number) VALUES ('Lili Anderson', 'bagijnhof 14', '3111KA', 'Schiedam', 'test@gmail.com', '0677283982')")
            self.cur.execute("INSERT INTO client (fullname, address, zipcode, city, email, phone_number) VALUES ('Anne Banwarth', 'bagijnhof 14', '3111KA', 'Schiedam', 'test@gmail.com', '0677283982')")
            self.conn.commit()
        except Exception as e: 
            print(e)

        # create user table if it does not exist
        tb_create = "CREATE TABLE users (username TEXT, password TEXT, firstname TEXT, lastname TEXT, admin INT, system_admin INT, advisor INT, joinDate TIMESTAMP);"
        try:
            self.cur.execute(tb_create)
            # add sample records to the db manually
            self.cur.execute("INSERT INTO users (username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES ('superadmin', 'Admin!23', 'admin', '', 1, 0, 0,'2021-10-25 18:09:12.091144')")
            self.cur.execute("INSERT INTO users (username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES ('ivy_russel', 'ivy@R123' , 'Ivy Russel', '', 0, 0, 1,'2021-10-25 18:09:12.091144')")
            self.cur.execute("INSERT INTO users (username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES ('test', 'test' , 'test account', '', 1, 0, 0,'2021-10-25 18:09:12.091144')")
            self.conn.commit()
        except Exception as e: 
            print(e)

    def login(self):
        global user_type, username
        username = input("please enter username: ").lower()
        password = input("please enter password: ")
        
        # string concatenation
        # sql_statement = f"SELECT * from users WHERE username='{username}' AND password='{password}'"
        # sql_statement = f'SELECT * from users WHERE username="{username}" AND password="{password}"'
        
        #PREPARED STATEMENT 1 (qmark style)
        sql_statement = ("SELECT * from users WHERE username = ? AND password = ?", (username, password))
        #Prepared statement 2 (named style)
        # self.cur.execute("SELECT * from users WHERE username=:username AND password=:password",  
        # {"username": username, "password": password})
        
        try:
            self.cur.execute("SELECT * from users WHERE username = ? AND password = ?", (username, password))
        
        except OperationalError as ErrorMessage:
            # print(ErrorMessage)
            print("Invalid input")
            #log the error message


        loggedin_user = self.cur.fetchone()
        if not loggedin_user:  # An empty result evaluates to False.
            print("Login failed")
        else:
            self.loggedin = 1
            self.loggedin_user = username
            if(loggedin_user[4] == 1):
                user_type = 'Admin'
            elif(loggedin_user[5] == 1):
                user_type = 'system_admin'
            else:
                user_type = 'advisor'
            # self.admin_is_loggedin = loggedin_user[4]
            # user_type = 'Admin' if self.admin_is_loggedin == 1 else 'Not Admin'
            print('\n\n\n\nWelcome')
            heading = '▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄'  + '\n'   + \
                      '▍ '                                           + '\n'   + \
                      '▍ Username: ' + colored(self.loggedin_user, 'red')   + '\n'   + \
                      '▍ '                                           + '\n'   + \
                      '▍ User type: ' + colored(user_type, 'red')    + '\n'   + \
                      '▍ '                                           + '\n'   + \
                      '▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀'  + '\n'   + \
                      'User Menu'
            
            db_interface = user_interface(heading, db_menu)
            db_interface.run()
            del db_interface

    def show_all_clients(self):
        # print("being worked on ")

        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        clientCount = 1
        print('---List of Clients---')
        for row in self.cur.execute('SELECT * FROM client'):
            print('Client ' + str(clientCount) + ' = ' + row[1])
            clientCount += 1


    def show_all_users(self):
        # self.not_implemented(self.show_all_users)
        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        userCount = 1
        print('---List of Users---')
        for row in self.cur.execute('SELECT * FROM users ORDER BY admin, system_admin, advisor'):
            if(row[4] == 1):
                print('User ' + str(userCount) + ' = ' + row[0] + ' | Role: superadmin')
            elif(row[5]== 1):
                print('User ' + str(userCount) + ' = ' + row[0] + ' | Role: system admin')
            else:
                print('User ' + str(userCount) + ' = ' + row[0] + ' | Role: advisor')
            userCount += 1
    
    def add_new_client(self):
        # self.not_implemented(self.add_new_client)        
        
        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        fullname = input('Please enter fullname: ')
        print('fullname = ' + fullname)
        address = input('Please enter address: ')
        print('address = ' + address)
        zipcode = validateZip()
        print('zipcode = ' + zipcode)

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
        print('City = ' + str(city))
        eMail = input('Please enter email address: ')
        print('Email is ' + eMail)

        phoneNumber = validatePhone()
        print('Phone number is ' + str(phoneNumber))
        
        entry = (fullname, address, zipcode, city, eMail, phoneNumber)
        
        try:
            self.cur.execute("INSERT INTO client(fullname, address, zipcode, city, email, phone_number) VALUES (?,?,?,?,?,?)", entry)
            self.conn.commit()
            print('Client sucessfully added.')

        except Exception as e:
            print(e)






    
    def add_new_user(self):
        #system_admin -> add advisor
        user_name = validateUser()
        passw = validatePassword()
        firstname = input('enter firstname: ')
        lastname = input('enter lastname: ')
        isAdvisor = 1
        isSysadmin = 0
        timestamp = datetime.now()

        testtuple = (user_name,passw,firstname,lastname,isAdvisor,isSysadmin,isAdvisor,timestamp)

        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()

        try:
            self.cur.execute("INSERT INTO users(username, password, firstname, lastname, admin, system_admin, advisor, joinDate) VALUES (?,?,?,?,?,?,?,?)", testtuple)
            self.conn.commit()
            print('User sucessfully added.')

        except Exception as e:
            print(e)
    
    def deleteAdvisor(self):
        
        user_name = searchAdvisor(self)
        try:
            self.cur.execute("DELETE FROM users WHERE username = ?", (user_name, ))
            self.conn.commit()
            print('User sucessfully Deleted.')

        except Exception as e:
            print(e)

        return

        

    def make_a_user_admin(self):
        self.not_implemented(self.make_a_user_admin)       

    def delete_client(self):
        self.not_implemented(self.delete_client)

    def delete_user(self):
        self.not_implemented(self.delete_user)

    def change_password(self):
        # self.not_implemented(self.change_password)
        print('Please enter new password')
        newPass = validatePassword()

        try:
            self.cur.execute("UPDATE users SET password = ? WHERE username = ?", (newPass, username))
            self.conn.commit()
            print('Password updated successfully')

        except Exception as e:
            print(e)



    def update_client_info(self):
        
        print("which client do you want to update?")
        # self.conn = sqlite3.connect(self.db_name) 
        # self.cur = self.conn.cursor()

        client = searchClient(self)
        print('')
        columns = ['fullname','address','zipcode','city','email','phone number']
        count = 1
        try:
            for i in columns:
                print( '[' + str(count) + '] ' + i)
                count += 1
        except Exception as e:
            print(e)
        print('')
        while True:
            chosenNumber = input('Please enter which info you want to update 1-5: ')
            if(chosenNumber in ['1','2','3','4','5','6']):
                break
            else:
                print('Please enter a valid number')
        
        if(chosenNumber == '1'):
            changeFullname(self, client)
        elif(chosenNumber == '2'):
            changeAddress(self, client)
        elif(chosenNumber == '3'):
            changeZip(self, client)
        elif(chosenNumber == '4'):
            changeCity(self, client)
        elif(chosenNumber == '5'):
            changeEmail(self, client)
        else:
            changePhone(self, client)
        

    def get_client_info(self):
            client = searchClient(self)

            self.conn = sqlite3.connect(self.db_name) 
            self.cur = self.conn.cursor()
            info = ""
            try:

                count = 0
                for row in self.cur.execute("SELECT * FROM client WHERE fullname =?", (client,)):
                    info = row
            except Exception as e:
                print(e)

            print('---Client Info---\n')
            print('id = ' + str(info[0]))
            print('fullname = ' + info[1])
            print('address = ' + info[2])
            print('zipcode = ' + info[3])
            print('city = ' + info[4])
            print('email = ' + info[5])
            print('phone number = ' + info[6])

            return
    
    def reset_advisor_password(self):

        advisor_name = searchAdvisor(self)
        self.conn = sqlite3.connect(self.db_name) 
        self.cur = self.conn.cursor()
        temp_psw = 'Welkom@01'

        print("Advisor password will be set to temporary password Welkom@01")

        try:
            self.cur.execute("UPDATE users SET password = ? WHERE username = ?", (temp_psw, advisor_name))
            self.conn.commit()
            print('password updated successfully')

        except Exception as e:
                print(e)
        return        

    def update_advisor_info(self):
        
        print('Which advisor do you want to update?')
        advisor_name = searchAdvisor(self)

        columns = ['username','password','firstname','lastname']

        count =1
        try:
            for i in columns:
                print( '[' + str(count) + '] ' + i)
                count += 1
        except Exception as e:
            print(e)
        print('')
        while True:
            chosenNumber = input('Please enter which info you want to update 1-4: ')
            if(chosenNumber in ['1','2','3','4']):
                break
            else:
                print('Please enter a valid number')
        
        if(chosenNumber == '1'):
            changeUsername(self, advisor_name)
        elif(chosenNumber == '2', advisor_name):
            changePassword(self)
        elif(chosenNumber == '3'):
            changeFirstname(self)
        else:
            changeLastname(self)


        
            











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
main_menu = [[1, 'login', client.login ], [0, 'Exit', client.close]]
db_menu = [ [1, 'show all clients', client.show_all_clients], [2, 'show all users', client.show_all_users], \
            [3, 'add new client', client.add_new_client], [4, 'add new user', client.add_new_user], \
            [5, 'make a user "admin"', client.make_a_user_admin], \
            [6, 'delete a client', client.delete_client], [7, 'delete a advisor', client.deleteAdvisor], \
            [8, 'change password', client.change_password],[9, 'reset advisor password', client.reset_advisor_password], [10, 'update client info', client.update_client_info], \
            [11,'update advisor info', client.update_advisor_info],[12, 'search client info',client.get_client_info], [0, 'logout', client.logout]]