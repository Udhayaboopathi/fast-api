from fastapi import FastAPI
import psycopg2

app = FastAPI()
def create_connection():
    try:
        conn = psycopg2.connect(
            database="form_data",
            host="localhost",
            user="postgres",
            password="udhaya",
            port="7000"  
        )
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
        return None 
    
table_name = "contact_data"

def table_create():
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                age INT,
                email VARCHAR(100),
                message VARCHAR(100)
            );
        '''.format(table_name)
        create_register_table_query = '''
            CREATE TABLE IF NOT EXISTS Register (
                id SERIAL PRIMARY KEY,
                username VARCHAR(100),
                password VARCHAR(100)
            );
        '''
        
        cursor.execute(create_table_query)
        cursor.execute(create_register_table_query)
        conn.commit()

        cursor.close()
        conn.close()
        print("Table created")
    else:
        print("Database not connected")
table_create()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    query = 'SELECT * FROM {}'.format(table_name)
    cursor.execute(query)
    users_data = cursor.fetchall()
    conn.close()
    return users_data

@app.get("/all")
def all_data():
    users_data = get_all_users()
    if users_data:
        users_list = []
        for user_data in users_data:
            user_dict = {
                'id': user_data[0],
                'name': user_data[1],
                'age': user_data[2],
                'email': user_data[3],
                'message': user_data[4]
                }
            users_list.append(user_dict)
        return user_data
    else:
        return user_data 

