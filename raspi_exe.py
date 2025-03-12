#FOR RASPBERRY PI

#install pyserial

import db_identity_verification
import db_identity
import time

import serial
import socket
import datetime

#_____________________________________________________________________________________#

#ARDUINO CONEXION
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1) 
# si no funciona probar con:
#                         /dev/ttyCOM0 ex: COM3 o COM4(el último es el mas normal)

scanner_input = 0 
verification_id = scanner_input  
people_id = 1  
pase = False
clase = "invalid"
#_____________________________________________________________________________________#
def while_running(verification_id, people_id):
    print("\n\n\n\n\n\n\n\n")
    conn, c = db_identity.create_connection()
    
    try:    
        while True:
            arduino_communication_verification()
            scanner_input = input()
            verification_id = scanner_input
            c.execute("SELECT id FROM people WHERE id = %s", (verification_id,))
            print("verification id:", verification_id,". READED")
            fetch = c.fetchone()
            (people_id) = fetch
            if people_id is not None:
                people_id = fetch[0]
                print("people id: ", people_id)
            else:
                print("people id: ", people_id)
                
            
            if people_id == None:
                print("This is your last chance, try again")
                verification_id2 = input()
                c.execute("SELECT id FROM people WHERE id = %s", (verification_id2,))
                people_id = c.fetchone()
                print("people id:", "Invalid")

                if people_id == None:
                    print("\n\nINTRUDE FOUND\n ...Initializing WARNING MODE\n")
                    arduino_communication_warning() #WARNING MODE
                    print("people id:", "Invalid")
                    get_dbinfo(verification_id)
                    while_running(verification_id, people_id)
                    
                else:
                    print("Match found, the communication is working")
                    arduino_communication_pass()
                    time.sleep(35)
                    get_dbinfo(verification_id)
                    while_running(verification_id, people_id)
            else:
                print("Match found, the communication is working")
                arduino_communication_pass()
                time.sleep(35)
                get_dbinfo(verification_id)
                while_running(verification_id, people_id)
                
    except Exception as e:
        print(f"Error from while_running: {e}")
    
    finally:
        db_identity.close_connection(conn, c)
        scanner_input
        verification_id = scanner_input      #id from scanner
        people_id = 1
        pase = False
        write_read("VERIFICATION_MODE_TRUE")
        print("System Closed\n")
        
        
        
def get_dbinfo(id):
    try:
        connn, cc = db_identity_verification.create_connection()
        conn, c = db_identity.create_connection()
        
        #time
        now = datetime.datetime.now()
        tiempo = now
        print(f"Time: {tiempo}")
        
        
        #ip
        get_ip = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        get_ip.connect(("2001:4860:4860::8888", 69)) #google dns, ramdom port (no le hagas caso a lo que dice y ya)
        ip = get_ip.getsockname()[0] #get ipv6
        print(f"IPv6: {ip}")
        
        #boolean/pase
        global pase
        
        #info
        get_info = cc.execute("SELECT count(*) FROM db_identity.verification WHERE true = true")
        get_info = cc.fetchone()
        info_base= get_info[0]
        info = info_base + 1
        print(info)
        
        #id
        try:
            get_id = c.execute("SELECT id FROM people WHERE id = %s", (id,))
            get_id = c.fetchone()
            if get_id is not None:
                id = get_id[0]
            else:
                id = None
        except Exception as e:
            print(f"No id:{id} Found,{e}")
            
            
        #CLASES   
        #clases: student, staff, guest, invalid.
        global clase
        
        if id is not None:
            get_class = c.execute("SELECT class FROM people WHERE id = %s", (id,))
            get_class = c.fetchone()
            clase = str(get_class[0])
        else:
            clase = "invalid" 
            
        #inserting  db
        cc.execute("INSERT INTO verification (date_time, ip_ipv6, pass, class, info, id) VALUES (%s, %s, %s, %s, %s, %s)", (tiempo, ip, pase, clase, info, id,))
        connn.commit()
    except Exception as e:
        print("Error from get_dbinfo in general: {e}")
    finally: 
        connn, cc = db_identity_verification.create_connection()
        conn, c = db_identity.create_connection()   
    
def write_read(x): 
	arduino.write(bytes(x, 'utf-8')) 
	time.sleep(0.05) 
	data = arduino.readline() 
	return data 

def arduino_communication_verification():
    print("VERIFICATION MODE\n\n>")
    write_read("VERIFICATION_MODE_TRUE")
    
def arduino_communication_tryagain():
    print("TRY AGAIN MODE\n\n>")
    write_read("TRY_AGAIN_MODE")
    
def arduino_communication_warning():
    global pase, clase
    pase = False
    clase = "invalid"
    print("WARNING MODE\n\n>")
    write_read("WARNING_MODE") 
    write_read("VERIFICATION_MODE_FALSE")
    
def arduino_communication_pass():
    try:
        #connn, cc = db_identity_verification.create_connection()
        #cc.execute("SELECT id FROM people WHERE id = %s", (verification_id,))
        global pase
        pase = True
        print("PASS MODE\n\n>")
        write_read("PASS_MODE")
        write_read("VERIFICATION_MODE_FALSE")
       
    except Exception as e:
        print(f"Error {e}")   
        
    finally:
        pass
        #db_identity_verification.close_connection(connn, cc) 
    
    
    #codigo, para cuando termine
    
while_running(verification_id, people_id)
print("its working") 
              	         