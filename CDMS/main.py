from ui import *
from database import * 

main_heading = '''
██████████████████████████████████████████████
█                                            █
█                 MY COMPANY                 █
█                 ----------                 █
█             Administration System          █

█                                            █
██████████████████████████████████████████████





Main Menu'''


main_interface = user_interface(main_heading, menueitems = main_menu)

if __name__ == "__main__":
    main_interface.run()





