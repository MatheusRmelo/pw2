from flask import Flask, render_template, request, redirect
import sqlite3

TEMPLATE = './templates'
STATIC = './static'
DB = './database.db'

app = Flask(__name__,static_url_path='',template_folder=TEMPLATE,static_folder=STATIC)

@app.route("/")
def welcome():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM users;
""")
    users = cursor.fetchall()
    conn.close()
    return render_template("index.html", users=users)
@app.route("/user-edit/<userId>")
def editUser(userId):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cQuery = "SELECT * FROM users WHERE id = %s;" % (userId)
    cursor.execute(cQuery)
    user = cursor.fetchone()
    conn.close()
    return render_template("update-user.html", user=user)
@app.route('/users-add', methods=['POST'])
def userAdd():
    name = request.form.get('name')
    email= request.form.get('email')
    jobTitle= request.form.get('jobTitle')

    cQuery = "INSERT INTO users(name,email,jobTitle) VALUES('%s','%s','%s');" % (name,email,jobTitle)

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(cQuery)
    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/users-delete', methods=['POST'])
def userDelete():
    userId = request.form.get('id')
    cQuery = "DELETE FROM users WHERE id =%s" % (userId)
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(cQuery)
    conn.commit()
    conn.close()

    return redirect('/')
@app.route('/users-update', methods=['POST'])
def userEdit():
    userId = request.form.get('id')
    name = request.form.get('name')
    email = request.form.get('email')
    jobTitle = request.form.get('jobTitle')

    conn = sqlite3.connect(DB)
    cQuery = "UPDATE users SET name='%s',email='%s',jobTitle='%s' WHERE id=%s;" % (name,email,jobTitle, userId)
    cursor = conn.cursor()
    cursor.execute(cQuery)
    conn.commit()
    conn.close()

    return redirect('/')

app.run()

