from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import webbrowser
import threading

app = Flask(__name__)

# Connect to database
def connect_db():
    conn = sqlite3.connect('inventory.db')
    return conn

# Route for landing page
@app.route('/')
def home():
    return render_template('index.html')

# Route for viewing inventory
@app.route('/inventory', methods=['GET', 'POST'])
def inventory():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    inventory_list = cursor.fetchall()
    return render_template('inventory.html', items=inventory_list)
# Insert item into inventory
@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = request.form['quantity']
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, quantity) VALUES (?, ?)", (name, quantity))
    conn.commit()
    return redirect(url_for('inventory'))

# Delete item from inventory
@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    return redirect(url_for('inventory'))

# Automatically open the browser after the app starts
def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
