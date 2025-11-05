from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import pooling
from config import DB_CONFIG

app = Flask(__name__)
app.secret_key = 'replace-with-a-secure-secret'  # change for production

# Connection pool
cnxpool = pooling.MySQLConnectionPool(pool_name="mypool",
                                      pool_size=5,
                                      **DB_CONFIG)

def get_conn():
    return cnxpool.get_connection()

@app.route('/')
def index():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    cur.execute("SELECT * FROM products ORDER BY id DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', products=rows)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name'].strip()
        category = request.form.get('category', 'General').strip()
        quantity = int(request.form.get('quantity', 0))
        price = float(request.form.get('price', 0.0))
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("INSERT INTO products (name, category, quantity, price) VALUES (%s, %s, %s, %s)",
                    (name, category, quantity, price))
        conn.commit()
        cur.close()
        conn.close()
        flash('Product added successfully', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:pid>', methods=['GET', 'POST'])
def edit(pid):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name'].strip()
        category = request.form.get('category', 'General').strip()
        quantity = int(request.form.get('quantity', 0))
        price = float(request.form.get('price', 0.0))
        cur.execute("UPDATE products SET name=%s, category=%s, quantity=%s, price=%s WHERE id=%s",
                    (name, category, quantity, price, pid))
        conn.commit()
        cur.close()
        conn.close()
        flash('Product updated', 'success')
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM products WHERE id=%s", (pid,))
    product = cur.fetchone()
    cur.close()
    conn.close()
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('index'))
    return render_template('edit.html', product=product)

@app.route('/delete/<int:pid>', methods=['POST'])
def delete(pid):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM products WHERE id=%s", (pid,))
    conn.commit()
    cur.close()
    conn.close()
    flash('Product deleted', 'success')
    return redirect(url_for('index'))

@app.route('/sell/<int:pid>', methods=['POST'])
def sell(pid):
    # decrement quantity by 1 if available
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT quantity FROM products WHERE id=%s", (pid,))
    row = cur.fetchone()
    if not row:
        flash('Product not found', 'danger')
    else:
        qty = row[0]
        if qty > 0:
            cur.execute("UPDATE products SET quantity = quantity - 1 WHERE id=%s", (pid,))
            conn.commit()
            flash('Product sold (quantity decreased)', 'success')
        else:
            flash('No stock available', 'warning')
    cur.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
