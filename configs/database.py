import sqlite3

DB_NAME = "users.db"

# create db tables
def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Create "users" table
    
    '''
    user_id
    city
    '''
    
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                       user_id INTEGER PRIMARY KEY,
                       city TEXT
                   )
                   ''')
    
    conn.commit()
    conn.close()
    
# Verify if user exists in database
def user_exists(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT 1 FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    
    if result != None: return 1
    else: return 0
    
def new_user(id, city):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO users (user_id, city) VALUES (?, ?)", (id, city,))
    
    conn.commit()
    conn.close()
    
def getCity(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT city FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result[0]