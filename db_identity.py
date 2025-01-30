#FOR RASPBERRY PI


import pymysql
from pymysql.err import MySQLError
from time import sleep


def create_connection(): #account
    try:

        conn = pymysql.connect(
            host="localhost",
            user="dog",
            password="4404",
            database="db_identity",
            charset='utf8mb4'
        )
        print("CREATED CONECTION")
        
        c = conn.cursor()
        sleep(1)
        c.execute("SELECT 1")
        print("Database verified and accessible")
        return conn, c
    
    except MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None
        
        
def create_table(conn, c): 
    try:
        c.execute('''           
            CREATE TABLE IF NOT EXISTS people 
            (   
                `class` varchar(25) NOT NULL,
                `id` int NOT NULL,
                `name` varchar(255) NOT NULL,
                `lastname` varchar(255) NOT NULL,
                `mail` varchar(500),
                `photo` LONGBLOB,
                PRIMARY KEY (id),
                CONSTRAINT check_class CHECK (`class` IN ('student', 'staff', 'guest'))
            )
        ''')#copy
        
        
        conn.commit()
        print("Table created successfully")
        
    except MySQLError as e:
        print(f"Error creating table: {e}")
    
    
def close_connection(conn, c):
    try:
        if c:
            c.close()  # Cierra el cursor explícitamente
        if conn:
            conn.close()  # Cierra la conexión
            print("Closed Connection")
    except MySQLError as e:
        print(f"Error when closing connection: {e}")


if __name__ == "__main__":
    connection, cursor = create_connection()
    if connection and cursor:
        create_table(connection, cursor)
        close_connection(connection, cursor)