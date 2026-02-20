from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
submissions = []

@app.route("/", methods=["GET", "POST"])
def index():
    message=""
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("telephone")

        submissions.append({
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone                    
        })

        send_email(email, first_name, last_name, phone)

        message = "Успешно сте се пријавили!"
    return render_template("index.html", message=message)

def send_email(to_email, first_name, last_name, phone):
    sender_email = "drobnjakfilip0@gmail.com"
    sender_password = os.environ.get("EMAIL_PASSWORD")
    subject = "Потврда пријаве"
    body = f"Помаже Бог {first_name}, \n\nУспешно сте се пријавили за Пливање за Часни Крст Господњи!\n\nВаши подаци су:\nИме: {first_name}\nПрезиме: {last_name}\nБрој телефона: {phone}.\n\nСрдачно,\nДом културе СТАРИ КОЛАШИН"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)

@app.route("/submissions")
def show_submissions():
    return {"submissions": submissions}  # Flask će ovo vratiti kao JSON



if __name__ == "__main__":
    app.run(debug=True)
