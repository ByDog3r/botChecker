from sys import stdout
from time import sleep
from huepy import lightred, lightgreen

def banner():
    print(lightred("""
     /$$                           /$$                           /$$      
    | $$                          | $$                          | $$      
    | $$$$$$$  /$$   /$$  /$$$$$$$| $$$$$$$   /$$$$$$   /$$$$$$$| $$   /$$
    | $$__  $$| $$  | $$ /$$_____/| $$__  $$ /$$__  $$ /$$_____/| $$  /$$/
    | $$  \ $$| $$  | $$| $$      | $$  \ $$| $$$$$$$$| $$      | $$$$$$/ 
    | $$  | $$| $$  | $$| $$      | $$  | $$| $$_____/| $$      | $$_  $$ 
 /$$| $$$$$$$/|  $$$$$$$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$| $$ \  $$
|__/|_______/  \____  $$ \_______/|__/  |__/ \_______/ \_______/|__/  \__/
               /$$  | $$                                                  
              |  $$$$$$/                                                  
               \______/                                                   \n"""))
    
    for i in lightgreen("\t\t.bychecker is started\n\n"):
        stdout.write(i)
        stdout.flush()
        sleep(1.0 / 12)