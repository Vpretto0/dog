#FOR RASPBERRY PI

#install pyserial


import db_identity_verification
import db_identity

import serial
import datetime

#_____________________________________________________________________________________#

#ARDUINO CONEXION
#arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1) 
# si no funciona probar con:
#                         /dev/ttyCOM0 ex: COM3 o COM4(el último es el mas normal)

scanner_input = 0 
verification_id = scanner_input  
people_id = int(1)  
pase = False
clase = "invalid"
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
            people_id = int(fetch[0])
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
                    get_dbinfo(0, "0", 0, verification_id)
                    print("people id: ", people_id)
                    while_running(verification_id, people_id)
                    
                else:
                    print("Match found, the communication is working")
                    arduino_communication_pass()
                    get_dbinfo(0, "0", 0, verification_id)
                    while_running(verification_id, people_id)
            else:
                print("Match found, the communication is working")
                arduino_communication_pass()
                get_dbinfo(0, "0", 0, verification_id)
                while_running(verification_id, people_id)
    except Exception as e:
        print(f"Error from correct_id: {e}")
    
    finally:
        db_identity.close_connection(conn, c)
        scanner_input
        verification_id = scanner_input      #id from scanner
        people_id = 0
        pase = False
def get_dbinfo(tiempo, ip, info, id):
    try:
        connn, cc = db_identity_verification.create_connection()
        conn, c = db_identity.create_connection()
        
        #________________________________________________TIEMPO________________________________________________#
        now = datetime.datetime.now()
        tiempo = now
        print(f"Time: {tiempo}")
        #________________________________________________IPv6  ________________________________________________#
        
        #________________________________________________PASE  ________________________________________________#
        #boolean
        global pase
        #________________________________________________INFO  ________________________________________________#
        
        
        get_info = cc.execute("SELECT count(*) FROM db_identity.verification WHERE true = true")
        get_info = cc.fetchone()
        info_base= int(get_info[0])
        info = info_base + 1
        print(info)
        
        #________________________________________________ID FK ________________________________________________#
        try:
            get_id = c.execute("SELECT id FROM people WHERE id = %s", (id,))
            get_id = c.fetchone()
            if id is not None:
                id = int(get_id[0])
            else:
                id = None
        except Exception as e:
            print(f"No id:{id}Found,{e}")
        #________________________________________________CLASE ________________________________________________#
        #clases: student, staff, guest, invalid.
        global clase
        
        if id is not None:
            get_class = c.execute("SELECT class FROM people WHERE id = %s", (id,))
            get_class = c.fetchone()
            clase = str(get_class[0])
        else:
            clase = "invalid"
        #________________________________________________INSERT INTO___________________________________________#
        cc.execute("INSERT INTO verification (date_time, ip_ipv6, pass, class, info, id) VALUES (%s, %s, %s, %s, %s, %s)", (tiempo, ip, pase, clase, info, id,))
        connn.commit()
    except Exception as e:
        print("Error from get_dbinfo in general{e}")
    finally: 
        try:
            print(f"Uploading info from database FINALLY STEP: {tiempo}, {ip}, {pase}, {clase}, {info}, {id}") 
            connn, cc = db_identity_verification.create_connection()
            conn, c = db_identity.create_connection()  
        except Exception as e:
            print(f"Error from get_dbinfo_finally step{e}")
            connn, cc = db_identity_verification.create_connection()
            conn, c = db_identity.create_connection() 

def arduino_communication_tryagain():
    print("TRY AGAIN MODE")

def arduino_communication_warning():
    global pase, clase
    pase = False
    clase = "invalid"
    print("WARNING MODE")
    
    #codigo, para cuando termine
    
def arduino_communication_pass():
    try:
        #connn, cc = db_identity_verification.create_connection()
        #cc.execute("SELECT id FROM people WHERE id = %s", (verification_id,))
        global pase
        pase = True
        print("PASS MODE")
       
    except Exception as e:
        print(f"Error {e}")   
        
    finally:
        pass
        #db_identity_verification.close_connection(connn, cc) 
    
    
    #codigo, para cuando termine
    
while_running(verification_id, people_id)
print("its working") 
              	         