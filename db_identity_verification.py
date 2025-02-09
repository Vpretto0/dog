#install pymysql
#install time

import pymysql
from pymysql.err import MySQLError
from time import sleep


def create_connection(): #account
    try:

        connn = pymysql.connect(
            host="localhost",
            user="dog",
            password="4404",
            database="db_identity",
            charset='utf8mb4'
        )
        print("CREATED CONECTION")
        
        cc = connn.cursor()
        sleep(1)
        cc.execute("SELECT 1")
        print("Database verified and accessible(verification table)")
        return connn, cc
    
    except MySQLError as e:
        print(f"Error connecting to database: {e}(verification table)")
        return None
        
        
def create_table(connn, cc): 
    try:
        cc.execute('''           
            CREATE TABLE IF NOT EXISTS verification 
            (   
                `date_time` varchar(100) NOT NULL,
                `ip_ipv6` varchar(39) NOT NULL,
                `pass` tinyint(1) NOT NULL,
                `class` varchar(25) NOT NULL,
                `info` int NOT NULL,
                `id` int NOT NULL,
                FOREIGN KEY (id) REFERENCES people(id))
            )
        ''')#copy
        #constraint deleted: ,
                #CONSTRAINT check_class CHECK (`class` IN ('student', 'staff', 'guest')
        
        
        connn.commit()
        print("Table created successfully(verification table)")
        
    except MySQLError as e:
        print(f"Error creating table: {e}(verification table)")
    
    
def close_connection(connn, cc):
    try:
        if cc:
            cc.close()  # Cierra el cursor explícitamente
        if connn:
            connn.close()  # Cierra la conexión
            print("Closed Connection(verification table)")
    except MySQLError as e:
        print(f"Error when closing connection: {e}(verification table)")


if __name__ == "__main__":
    connection, cursor = create_connection()
    if connection and cursor:
        create_table(connection, cursor)
        close_connection(connection, cursor)