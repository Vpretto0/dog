import db_identity_verification
import db_identity
#_____________________________________________________________________________________#

verification_id = 0
people_id = 0

#_____________________________________________________________________________________#
def db_id_v():
    connn, cc = db_identity_verification.create_connection()
    try: 
        pass
        
    except Exception as e:
        pass
    
    finally:
        db_identity_verification.close_connection(connn, cc)
        
        
def db_id_p():
    try: 
        conn, c = db_identity.create_connection()
        
    except Exception as e:
        pass

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
    
    while scanner_input:
        print("while_running")
        connn, cc = db_identity_verification.create_connection()
        conn, c = db_identity.create_connection()
        if conn is not None and c is not None:
            pass
        else:
            print("THE LAW AND ORDER", "Error Entering to database")
        #if db_identity_verification  and db_identity:
        #if get table verification(id (FK(?))) == id_people (id PK from people)
            #make verification pass = True or 1 
            #arduino output: you pass = arduino say you pass or something
        #else: 
            #make verification pass = False or 0
            
            #if verification pass == False or 0:
                #serial communication output: try_again or(||) you_pass
                
                #try:
                    #input(again)
                        #if try_again:
                            #if get table verification(id (FK(?))) == id_people (id PK from people)
                                #make verification pass = True or 1 
                            #else: 
                                #make verification pass = False or 0
                                
                                #if verification pass == False or 0:
                                    #serial communication output: warning
                                    
                                            #= arduino things
                                
                    #exception as e:
                        #error +ó-
                            	

            
                    