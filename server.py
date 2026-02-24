from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
import os
import sqlite3



app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS korisnici(
          id INTEGER PRIMARY KEY,
          first_name TEXT NOT NULL,
          last_name TEXT NOT NULL,
          email TEXT NOT NULL,
          telephone TEXT)

          """)
    conn.commit()
    conn.close()


@app.route("/", methods=["GET", "POST"])
def index():
    message=""
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        telephone = request.form.get("telephone")
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("""
                INSERT INTO korisnici (first_name, last_name, email, telephone)
                VALUES (?,?,?,?)
            """, (first_name, last_name, email, telephone))
        conn.commit()
        conn.close()


        send_email(email, first_name, last_name, telephone)

        message = "Успешно сте се пријавили!"
    
        return redirect(url_for("success"))
    
    return render_template("index.html", message=message)

@app.route("/success")
def success():
    return render_template("success.html")

def send_email(email, first_name, last_name, phone):
    sender_email = "drobnjakfilip0@gmail.com"
    sender_password = os.environ.get("EMAIL_PASSWORD")
    subject = "Потврда пријаве"
    body = f"Помаже Бог {first_name}, \n\nУспешно сте се пријавили за Пливање за Часни Крст Господњи!\n\nВаши подаци су:\nИме: {first_name}\nПрезиме: {last_name}\nБрој телефона: {phone}.\n\nСрдачно,\nДом културе СТАРИ КОЛАШИН"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5500)
