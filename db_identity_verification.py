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
        print("Database verified and accessible(verification table)")
        return conn, c
    
    except MySQLError as e:
        print(f"Error connecting to database: {e}(verification table)")
        return None
        
        
def create_table(conn, c): 
    try:
        c.execute('''           
            CREATE TABLE IF NOT EXISTS verification 
            (   
                `date` varchar(10) NOT NULL,
                `hour` varchar(5) NOT NULL,
                `ip_ipv6` varchar(39) NOT NULL,
                `pass` tinyint(1) NOT NULL,
                `class` varchar(25) NOT NULL,
                `info` int NOT NULL,
                `id` int NOT NULL,
                FOREIGN KEY (id) REFERENCES people(id),
                CONSTRAINT check_class CHECK (`class` IN ('student', 'staff', 'guest'))
            )
        ''')#copy
        
        
        conn.commit()
        print("Table created successfully(verification table)")
        
    except MySQLError as e:
        print(f"Error creating table: {e}(verification table)")
    
    
def close_connection(conn, c):
    try:
        if c:
            c.close()  # Cierra el cursor explícitamente
        if conn:
            conn.close()  # Cierra la conexión
            print("Closed Connection(verification table)")
    except MySQLError as e:
        print(f"Error when closing connection: {e}(verification table)")


if __name__ == "__main__":
    connection, cursor = create_connection()
    if connection and cursor:
        create_table(connection, cursor)
        close_connection(connection, cursor)