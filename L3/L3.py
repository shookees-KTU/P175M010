# coding=utf-8
import base64
import os
from Steganography import ImageRandomizer, Image
from contextlib import closing
import random, string
import sqlite3
from flask import Flask, g, render_template, session, request, abort, flash, redirect, url_for

#paprasta konfiguracija
DATABASE = "/tmp/L3.db"
DEBUG = True
SECRET_KEY = "kriptografija"


app = Flask(__name__)
app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config["DATABASE"])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource("schema.sql") as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute("select title, text from entries order by id desc")
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template("show_entries.html", entries=entries)

@app.route("/add", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        abort(401)
    g.db.execute("insert into entries(title, text) values('{0}','{1}')".format(
                 request.form["title"].encode("utf-8"), request.form["text"].encode("utf-8")))
    g.db.commit()
    flash("Naujas įrašas sėkmingai išsaugotas")
    return redirect(url_for("show_entries"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        if request.form["username"]:
            cur = g.db.execute("select 1 from accounts where username='{0}'".format(request.form["username"]))
            if cur.rowcount > 0:
                error = "Vartotojo vardas jau egzistuoja"
            else:
                #sukuriamas paprastas irasas
                password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))
                cur = g.db.execute("insert into accounts(username, password) values('{0}', '{1}')".format(
                                   request.form["username"].encode("utf-8"), password))
                g.db.commit()

                id = str(int(cur.lastrowid)) + ".png"
                #bandom isideti paveiksleli
                if not ImageRandomizer.createRandomImage(id):
                    error = "Prasau bandyti iš naujo".encode("UTF-8")
                else:
                    Image.hide("/tmp/" + str(id), password)
                with open("/tmp/" + str(id), "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                #apsivalome
                #os.remove("images/" + str(id))
                return render_template("register.html", img=encoded_string)
        else:
            error = "Blogai uzpildyta forma".encode("UTF-8")

        if error:
            redirect(url_for("register"))
    elif request.method == "GET":
        return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        cur = g.db.execute("select password from accounts where username='{0}'".format(
                                   request.form["username"].encode("utf-8")))
        password = cur.fetchone()
        #gaunam paveiksliuka
        pic = request.files["file"]
        decodedPassword = Image.retrieve(pic)
        if password == None:
            error = "Neteisingas vardas"
        elif password[0] != decodedPassword:
            error = "Neteisingas slaptazodis"
        else:
            session["logged_in"] = True
            flash("Prisijungėte")
            return redirect(url_for("show_entries"))
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Atsijungėte")
    return redirect(url_for("show_entries"))


if __name__ == '__main__':
    app.run()
