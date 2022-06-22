from ui import *
from database import * 

main_heading = '''
██████████████████████████████████████████████
█                                            █
█                 MY COMPANY                 █
█                 ----------                 █
█             Furnicor Family System         █
█                                            █
██████████████████████████████████████████████



Main Menu'''


main_interface = user_interface( user_type, message, notification, main_heading, menueitems = main_menu)

if __name__ == "__main__":
    main_interface.run()
