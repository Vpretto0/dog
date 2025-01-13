import pymysql
from pymysql.err import MySQLError


def create_connection(): #account
    try:

        conn = pymysql.connect(
            host="localhost",
            user="dog",
            password="4404",
            database="db_identity",
            charset='utf8mb4'
        )
        
        
        c = conn.cursor()
        print("CREATED CONECTION")
        if conn.is_connected():
            print("Successful connection to database")
        
        c.execute('''           
            CREATE TABLE IF NOT EXISTS people 
            (   
                `class` varchar(25) NOT NULL,
                `id` int NOT NULL,
                `name` varchar(255) NOT NULL,
                `last name` varchar(255) NOT NULL,
                `mail` varchar(500),
                `photo` LONGBLOB,
                PRIMARY KEY (id),
                CONSTRAINT check_class CHECK (`class` IN ('student', 'staff', 'guest'))
            )
        ''')#copy
        
        
        conn.commit()
        return conn
    
    
    except MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None
    

def close_connection(conn): #close conection
    if conn:
        conn.close()
        print("Closed Connection")



if __name__ == "__main__":
    connection = create_connection()
    if connection:
        close_connection(connection)