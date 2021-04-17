## 모듈 불러오기 ##
#flask
from flask import Flask, render_template, request, session
import pymysql, json, smtplib, random
#이메일
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#암호화
from flask_bcrypt import Bcrypt


## default settings ##
#get hidden.js
with open("hidden.json", "r") as f:
    hidden = json.loads(f.read())

#connect to DB
def connectDb():
    return pymysql.connect(host="localhost", user="root", password=hidden["db"]["pw"])

## set app ##
#vuejs와 jinja 충돌 방지
class MyFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
        block_start_string='(%',
        block_end_string='%)',
        variable_start_string='((',
        variable_end_string='))',
        comment_start_string='(#',
        comment_end_string='#)',
    ))

app = MyFlask(__name__)
app.secret_key = hidden["app"]["key"]
app.config['BCRYPT_LEVEL'] = 5

bcrypt = Bcrypt(app)


## pages ##
#login
@app.route("/login/")
def login():
    return render_template("login/index.html")

#signup
@app.route("/signup/")
def signup():
    return render_template("signup/index.html")

#create_project
@app.route("/new/")
def newproject():
    return render_template("/newproject/index.html")


## api ##
#login
@app.route("/api/login/", methods=["POST"])
def api_login():
    #get body
    data = json.loads(request.data.decode())
    email = data["email"].replace(" ", "")
    pw = data["pw"]

    #connect DB
    conn = pymysql.connect(host="localhost", user="root", password=hidden["db"]["pw"])
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("USE logg2;")

    #select!
    cursor.execute("SELECT idx, email, password FROM account WHERE email='{email}';".format(email=email))
    account = cursor.fetchall()

    #check if email exists
    if len(account) == 0:
        return {"status": 404}

    #password
    if bcrypt.check_password_hash(account[0]["password"], pw):
        session["loggUserId"] = int(account[0]["idx"])
        return {"status": 200}

    else:
        #wrong password
        return {"status": 403}

    conn.close()

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
def api_signup():
    #get post information
    data = json.loads(request.data.decode())
    username = data["username"]
    password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
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
    cursor.execute('INSERT INTO account (username, password, created, description, email) VALUES ("{username}", "{password}", NOW(), "false", "{email}")'.format(username=username, password=password, email=email))

    conn.commit()
    conn.close()

    return "success"

@app.route("/api/new/", methods=["POST"])
def api_new():
    #POST body 가져오기
    body = json.loads(request.data)
    name = body["name"]
    desc = body["desc"]

    #DB 접속
    conn = connectDb()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("USE logg2;")

    #project 테이블에 insert
    cursor.execute("insert into project (name, description) values ('{name}', '{desc}');".format(name=name, desc=desc))

    #생성한 project의 아이디 확인하기
    cursor.execute("select last_insert_id() from project;")
    idx = int(cursor.fetchall()[0]["last_insert_id()"])
    cursor.execute("insert into project_people (userid, projectid, owner) values ({userid}, {projectid}, 1);".format(userid=session["loggUserId"], projectid=idx))

    conn.commit()
    conn.close()

    return {"status": 200}

## 기타 ##
@app.route("/template/")
def template():
    return render_template("template.html")

@app.route("/session/login/")
def session_login():
    return str(session["loggUserId"])

#debug mode
if __name__ == "__main__":
    app.run(debug=True)
