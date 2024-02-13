import os 
from colorama import init,Fore,Back,just_fix_windows_console

init()
just_fix_windows_console()

def banner():
    try:
        os.system("cls")
    except:
        os.system('clear')

    print(Fore.CYAN + """                                

    __  __           __             _   __                 
   / / / /___ ______/ /_____  _____/ | / /__ _      _______
  / /_/ / __ `/ ___/ //_/ _ \/ ___/  |/ / _ \ | /| / / ___/
 / __  / /_/ / /__/ ,< /  __/ /  / /|  /  __/ |/ |/ (__  ) 
/_/ /_/\__,_/\___/_/|_|\___/_/  /_/ |_/\___/|__/|__/____/  
                                                           
                                                        v0.1

""")