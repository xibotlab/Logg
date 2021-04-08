from flask import Flask, render_template, request, session
import pymysql, json, smtplib, random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_bcrypt import Bcrypt

## default settings ##
#get hidden.js
with open("hidden.json", "r") as f:
    hidden = json.loads(f.read())

#connect to DB
def connectDb():
    return pymysql.connect(host="localhost", user="root", password=hidden["db"]["pw"])

## set app ##
app = Flask(__name__)
app.secret_key = hidden["app"]["key"]
app.config['BCRYPT_LEVEL'] = 5

bcrypt = Bcrypt(app)

# pwhash = key.generate_password_hash("hunter2")
# print(pwhash)
# print(key.check_password_hash(pwhash, "hunter2"))


## pages ##
#login
@app.route("/login")
def login():
    return render_template("login/index.html")

#signup
@app.route("/signup/")
def signup():
    return render_template("signup/index.html")


## api ##
#login
@app.route("/api/login/", methods=["POST"])
def login_api():
    #get body
    data = json.loads(request.data.decode())
    email = data["email"].replace(" ", "")
    pw = data["pw"]

    #select!
    cursor.execute("SELECT email, password FROM account WHERE email='{email}';".format(email=email))
    account = cursor.fetchall()

    #check if email exists
    if len(account) == 0:
        return {"status": 404}
    
    #password
    if account[0]["password"] == pw:
        return {"status": 200}
    else:
        #wrong password
        return {"status": 403}

#이메일 인증
@app.route("/api/signup/verify/", methods=["GET", "POST"])
def signup_verify():
    #get query string
    data = json.loads(request.data.decode())
    adress = data["adress"]
    nickname = data["nickname"]
    verify = random.randint(1000, 9999)

    #세션에 인증번호를 저장
    session["verify"] = verify

    #SMTP 이메일 로그인
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("xibotlab@gmail.com", hidden["email"]["pw"])

    #인증 메일 전송하기
    msg = MIMEMultipart("alternative")
    msg["subject"] = "[Logg] 인증번호 발송"
    msg['From'] = 'xibotlab@gmail.com'
    msg['To'] = adress

    msg.attach(MIMEText(render_template("email/index.html", username=nickname, code=str(verify)), "html"))
    s.send_message(msg)

    s.quit()

    return {"status": 200}

@app.route("/api/signup/", methods=["POST"])
def signup_upload():
    #get post information
    data = json.loads(request.data.decode())
    username = data["username"]
    password = bcrypt.generate_password_hash(data["password"])
    email = data["email"]
    verify = data["verify"]

    #DB 로그인
    conn = connectDb()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("use logg2;")

    #인증번호 체크
    if not str(session["verify"]) == (verify):
        return "verifyerror" 

    #이미 존재하는 이메일인지 체크
    cursor.execute("SELECT email FROM account WHERE email='{email}';".format(email=email.replace(" ", "")))
    if len(cursor.fetchall()) > 0:
        return "emailerror"
    
    #load db password
    dbpw = hidden["db"]["pw"]

    #insert into db
    cursor.execute('INSERT INTO account (username, password, created, description, email) VALUES ("{username}", "{password}", NOW(), "false", "{email}")'.format(username=username, password=str(password), email=email))

    conn.commit()
    conn.close()

    return "success"

#debug mode
if __name__ == "__main__":
    app.run(debug=True)