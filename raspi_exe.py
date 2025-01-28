import db_identity_verification
import db_identity

#_____________________________________________________________________________________#

scanner_input = input()     #input from scanner
verification_id = scanner_input      #id from scanner
people_id = 0  # %s     #tiene que ser igual a verification_id si no = warning_cmd

#_____________________________________________________________________________________#
def correct_id(verification_id, people_id):
    conn, c = db_identity.create_connection()
    try: 
        c.execute("SELECT id FROM people WHERE id = %s", (verification_id,))
        print("verification id: ", verification_id,". READED")
        people_id = c.fetchone()
        print("people id: ", people_id)
        
    except Exception as e:
        print(f"Error from correct_id: {e}")
    
    finally:
        #db_identity_verification.close_connection(connn, cc)
        db_identity.close_connection(conn, c)
        

def db_check():
    try:
        connn, cc = db_identity_verification.create_connection()
        conn, c = db_identity.create_connection()
        if conn is not None and c is not None:
            if connn is not None and cc is not None:
                if verification_id == people_id:
                    pass
                
            
            
            else:
                print("THE LAW AND ORDER", "Error Entering to database(verification)")
        else:
            print("THE LAW AND ORDER", "Error Entering to database(people)")

    except Exception as e:
        pass


def arduino_communication():
    pass



def while_running(scanner_input):
    print("input readed: ", scanner_input)  
    if verification_id == people_id:
        pass
correct_id(verification_id, people_id)
print("its working") 
while_running(scanner_input)               	

            
                    