from flask import Flask, request, jsonify
import sqlite3
import re

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create tables if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS companies (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        user_id INTEGER,
        company_id INTEGER,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (company_id) REFERENCES companies (id)
    )
''')
conn.commit()

# Close database connection after each request
@app.teardown_appcontext
def close_connection(exception):
    if conn is not None:
        conn.close()

# Endpoint to list app users
@app.route('/users', methods=['GET'])
def list_users():
    username = request.args.get('username')
    cursor = conn.cursor()  # Create a new cursor for this request
    if username:
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    else:
        cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    return jsonify(users)

# Endpoint to update user fields
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    cursor = conn.cursor()  # Create a new cursor for this request
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    cursor.execute('UPDATE users SET username = ?, email = ? WHERE id = ?',
                   (data['username'], data['email'], user_id))
    conn.commit()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    updated_user = cursor.fetchone()
    return jsonify(updated_user)

# Endpoint to create a client
@app.route('/clients', methods=['POST'])
def create_client():
    data = request.json
    if not all(key in data for key in ['name', 'user_id', 'company_id', 'email', 'phone']):
        return jsonify({'error': 'Missing required fields'}), 400
    if not re.match(r'^[\w\.-]+@[\w\.-]+$', data['email']):
        return jsonify({'error': 'Invalid email format'}), 400
    cursor = conn.cursor()  # Create a new cursor for this request
    cursor.execute('INSERT INTO clients (name, user_id, company_id, email, phone) VALUES (?, ?, ?, ?, ?)',
                   (data['name'], data['user_id'], data['company_id'], data['email'], data['phone']))
    conn.commit()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (cursor.lastrowid,))
    client = cursor.fetchone()
    return jsonify(client), 201

# Endpoint to update client fields
@app.route('/clients/<int:client_id>', methods=['PATCH'])
def update_client(client_id):
    data = request.json
    cursor = conn.cursor()  # Create a new cursor for this request
    cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
    client = cursor.fetchone()
    if client is None:
        return jsonify({'error': 'Client not found'}), 404
    field_updates = ', '.join(f"{key} = '{value}'" for key, value in data.items())
    cursor.execute(f'UPDATE clients SET {field_updates} WHERE id = ?', (client_id,))
    conn.commit()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (client_id,))
    updated_client = cursor.fetchone()
    return jsonify(updated_client)

# Endpoint to search for companies by employees range
@app.route('/companies', methods=['GET'])
def search_companies_by_employees():
    min_employees = request.args.get('min_employees')
    max_employees = request.args.get('max_employees')
    cursor = conn.cursor()  # Create a new cursor for this request
    cursor.execute('SELECT * FROM companies')
    companies = cursor.fetchall()
    return jsonify(companies)

# Endpoint to search for clients by user or name
@app.route('/clients/search', methods=['GET'])
def search_clients():
    user_id = request.args.get('user_id')
    name = request.args.get('name')
    cursor = conn.cursor()  # Create a new cursor for this request
    if user_id:
        cursor.execute('SELECT * FROM clients WHERE user_id = ?', (user_id,))
    elif name:
        cursor.execute('SELECT * FROM clients JOIN companies ON clients.company_id = companies.id WHERE companies.name LIKE ?', ('%' + name + '%',))
    else:
        return jsonify({'error': 'Provide either user_id or name parameter'}), 400
    clients = cursor.fetchall()
    return jsonify(clients)

if __name__ == '__main__':
    app.run(debug=True)
