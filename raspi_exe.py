#FOR RASPBERRY PI


import db_identity_verification
import db_identity

import serial

#_____________________________________________________________________________________#

#ARDUINO CONEXION
#arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1) 
# si no funciona probar con:
#                         /dev/ttyCOM0 ex COM3 o COM4(el ultimo es el mas normal)

scanner_input = 0 
verification_id = scanner_input  
people_id = int(1)  

#_____________________________________________________________________________________#
def while_running(verification_id, people_id):
    conn, c = db_identity.create_connection()
    
    try:    
        while True:
            scanner_input = int(input())
            verification_id = scanner_input
            
            c.execute("SELECT id FROM people WHERE id = %s", (verification_id,))
            print("verification id:", verification_id,". READED")
            fetch = c.fetchone()
            (people_id) = fetch
            print("people id: ", people_id)
            
            if people_id == None:
                print("This is your last chance, try again")
                verification_id2 = input()
                c.execute("SELECT id FROM people WHERE id = %s", (verification_id2,))
                people_id = c.fetchone()
                print("people id: ", people_id)
                
                if people_id == None:
                    print("\n\nINTRUDE FOUND\n ...Initializing WARNING MODE\n")
                    arduino_communication_warning() #WARNING MODE
                    
                    print("people id: ", people_id)
                    while_running(verification_id, people_id)
                    
                else:
                    print("Match found, the communication is working")
                    arduino_communication_pass()
                    while_running(verification_id, people_id)
            else:
                print("Match found, the communication is working")
                arduino_communication_pass()
                while_running(verification_id, people_id)
    except Exception as e:
        print(f"Error from correct_id: {e}")
    
    finally:
        db_identity.close_connection(conn, c)
        scanner_input
        verification_id = scanner_input      #id from scanner
        people_id = 0
        

def arduino_communication_tryagain():
    print("TRY AGAIN MODE")

def arduino_communication_warning():
    print("WARNING MODE")
    
    #codigo, para cuando termine
    
def arduino_communication_pass():
    print("PASS MODE")
    
    #codigo, para cuando termine
    


    

while_running(verification_id, people_id)
print("its working") 
              	

            
                    