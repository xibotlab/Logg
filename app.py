from flask import Flask, render_template, request
import pymysql, json, smtplib, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

#hidden 불러오기
with open("hidden.json", "r") as f:
    hidden = json.loads(f.read())

#signup
@app.route("/signup")
def signup():
    return render_template("signup/index.html")

@app.route("/signup/verify", methods=["GET", "POST"])
def signup_verify():
    #get query string
    data = json.loads(request.data.decode())
    adress = data["adress"]
    nickname = data["nickname"]
    key = data["key"]
    verify = random.randint(1000, 9999)

    #key의 value를 DB에 저장
    conn = pymysql.connect(host="localhost", user="root", password=hidden["db"]["pw"])
    cursor = conn.cursor()
    cursor.execute("USE logg2;")
    cursor.execute("INSERT INTO verify (idx, value) VALUES ('{key}', {value})".format(key=key, value=verify))
    conn.commit()
    conn.close()

    #login
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("xibotlab@gmail.com", hidden["email"]["pw"])

    #send
    msg = MIMEMultipart("alternative")
    msg["subject"] = "[Logg] 인증번호 발송"
    msg['From'] = 'xibotlab@gmail.com'
    msg['To'] = adress

    msg.attach(MIMEText(render_template("email/index.html", username=nickname, code=str(verify)), "html"))
    s.send_message(msg)

    s.quit()

    return {"status": 200}

@app.route("/signup/upload", methods=["POST"])
def signup_upload():
    #get post information
    data = json.loads(request.data.decode())
    username = data["username"]
    password = data["password"]
    email = data["email"]
    key = data["key"]
    verify = data["verify"]

    #DB 로그인
    conn = pymysql.connect(host="localhost", user="root", password=hidden["db"]["pw"])
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("use logg2;")

    #인증번호 체크
    cursor.execute("SELECT * FROM verify WHERE idx='{key}';".format(key=key))
    if not str(cursor.fetchall()[0]["value"]) == str(verify):
        return "verifyerror"

    #이미 존재하는 이메일인지 체크
    cursor.execute("SELECT email FROM account WHERE email='{email}';".format(email=email.replace(" ", "")))
    if len(cursor.fetchall()) > 0:
        return "emailerror"
    
    #load db password
    dbpw = hidden["db"]["pw"]

    #connect to db
    conn = pymysql.connect(host="localhost", user="root", password=dbpw)
    cursor = conn.cursor()
    cursor.execute("USE logg2;")

    #insert into db
    cursor.execute('INSERT INTO account (username, password, created, description, img, email) VALUES ("{username}", "{password}", NOW(), "false", "false", "{email}")'.format(username=username, password=password, email=email))

    conn.commit()
    conn.close()

    return "success"

#etc
@app.route("/email")
def email():
    return render_template("email/index.html", username="helloworld", code="111111")

#debug mode
if __name__ == "__main__":
    app.run(debug=True)