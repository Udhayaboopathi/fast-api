from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()

class login_data (BaseModel):
    name: str
    age: int = None
    email: str 
    message: str = None

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
        return users_list
    else:
        return user_data 
       
@app.post('/submit_form')
def submit_form(login_data: login_data):
    name = login_data.name
    age = login_data.age
    email = login_data.email
    message = login_data.message
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {} WHERE email = %s".format(table_name), (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            cursor.close()
            conn.close()
            return ({"message": "This email is already stored."})
        else:
            query = "INSERT INTO {} (name, age, email, message) VALUES (%s, %s, %s, %s)".format(table_name)
            cursor.execute(query, (name, age, email, message))
            conn.commit()
            cursor.close()
            conn.close()
            print("Data saved")
            return ({"message": "Data stored successfully"})
    else:
        return ({"error": "Failed to connect to the database"})
    
    
@app.put("/update/{user_id}")
def update_user(user_id: int, new_data: login_data):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {} WHERE id = %s".format(table_name), (user_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            # Extracting new data
            name = new_data.name
            age = new_data.age
            email = new_data.email
            message = new_data.message
            
            # Updating user data
            update_query = '''
                UPDATE {} 
                SET name = %s, age = %s, email = %s, message = %s 
                WHERE id = %s
            '''.format(table_name)
            cursor.execute(update_query, (name, age, email, message, user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return {"message": "User data updated successfully"}
        else:
            cursor.close()
            conn.close()
            return {"error": "User not found"}
    else:
        return {"error": "Failed to connect to the database"}

@app.delete("/delete/{user_id}")
def delete_user(user_id: int):
    conn = create_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM {} WHERE id = %s".format(table_name), (user_id,))
        existing_user = cursor.fetchone()
        if existing_user:
            delete_query = "DELETE FROM {} WHERE id = %s".format(table_name)
            cursor.execute(delete_query, (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return {"message": "User deleted successfully"}
        else:
            cursor.close()
            conn.close()
            return {"error": "User not found"}
    else:
        return {"error": "Failed to connect to the database"}


