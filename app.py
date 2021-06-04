## 모듈 불러오기 ##
from flask import Flask, render_template, request, session, redirect, send_file
from werkzeug.utils import secure_filename
import pymysql, json, random, os
#암호화
from flask_bcrypt import Bcrypt

import api

with open("hidden.json", "r") as f:
    hidden = json.loads(f.read())

#인스턴스 생성
account = api.account()
project = api.project()
db = api.db()
dbaccount = api.db.account()

## set app ##
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
app.config["UPLOAD_FOLDER"] = "file/"

bcrypt = Bcrypt(app)


## pages ##
#login
@app.route("/login/")
def login():
    return render_template("account/login/index.html")

#signup
@app.route("/signup/")
def signup():
    form = [
        {"id": "email", "title": "이메일", "type": "text", "placeholder": "이메일을 입력해주세요..."},
        {"id": "nickname", "title": "닉네임", "type": "text", "placeholder": "실명을 입력하지 마세요."},
        {"id": "pw", "title": "비밀번호", "type": "password", "placeholder": "아무에게도 알려주지 마세요."},
        {"id": "pwagain", "title": "비밀번호 재입력", "type": "password", "placeholder": "다시 비밀번호를 입력합니다."}
    ]
    return render_template("account/signup/index.html", form=form)

#create_project
@app.route("/new/")
def newproject():
    return render_template("/project/new/index.html")

#project page
@app.route("/project/<idx>/")
def projectPage(idx):
    cursor = db.connect().cursor(pymysql.cursors.DictCursor)
    cursor.execute("use logg2;")
    cursor.execute("select * from project where idx={idx};".format(idx=idx))
    project = cursor.fetchall()

    if len(project) == 0:
        return "404 Not Found", 404
    else:
        return render_template("/project/index.html", idx=idx, name=project[0]["name"])

#project settings
SettingMenu = ["기본정보", "개인정보"]
@app.route("/project/settings/<idx>/")
def project_settings(idx):
    cursor = db.connect().cursor(pymysql.cursors.DictCursor)
    cursor.execute("use logg2;")
    
    #name 가져오기
    cursor.execute("select name from project where idx={idx};".format(idx=idx))
    name = cursor.fetchall()[0]["name"]

    #description 가져오기
    cursor.execute("select description from project where idx={idx};".format(idx=idx))
    desc = cursor.fetchall()[0]["description"]

    return render_template("/project/settings/index.html", idx=idx, selected=None, category=SettingMenu, name=name, desc=desc)

## api ##
@app.route("/api/img/<idx>/")
def api_img(idx):
    return send_file("./file/{idx}.png".format(idx=idx), mimetype="image/png")

#login
@app.route("/api/login/", methods=["POST"])
def api_login():
    #get body
    data = json.loads(request.data.decode())
    email = data["email"].replace(" ", "")
    pw = data["pw"]
    
    account = dbaccount.email(email)
    #아이디가 존재하지 않다면:
    if account == False:
        return {"status": 404}
    elif not bcrypt.check_password_hash(account["password"], pw):
        return {"status": 403}
    else:
        session["loggUserId"] = account["idx"]
        return {"status": 200}


#이메일 인증
@app.route("/api/signup/verify/", methods=["GET", "POST"])
def signup_verify():
    #get query string
    data = json.loads(request.data.decode())
    email = data["adress"]
    nickname = data["nickname"]
    code = random.randint(1000, 9999)

    #세션에 인증번호를 저장
    session["verify"] = code

    if account.sendverify(email, nickname, code):
        return {"status": 200}, 200
    else:
        return {"status": 500}, 500

@app.route("/api/signup/", methods=["POST"])
def api_signup():
    #body 가져오기
    data = json.loads(request.data.decode())
    email = data["email"]
    nickname = data["username"]
    pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    code = int(data["verify"])

    #인증번호 체크
    if not session["verify"] == int(code):
        return {"status": 403}, 403
        
    return {"status": account.signup(email, nickname, pw)}

@app.route("/api/project/new/", methods=["POST"])
def api_new():
    #기본 변수 지정
    body = json.loads(request.data)
    name = body["name"]
    desc = body["desc"]

    # 로그인 여부 확인
    try: userid = session["loggUserId"]
    except: return {"status": 403}, 403

    return {"status": project.new(name, desc, session["loggUserId"])}

@app.route("/api/project/update/name/", methods=["POST"])
def update_project_name():
    #get BODY
    body = json.loads(request.data.decode())
    idx = body["idx"]
    name = body["name"]

    result = project.update(idx, "name", name)
    if result:
        return {"status": 200}
    elif result == 404:
        return {"status": 404}

@app.route("/api/project/update/desc/", methods=["POST"])
def update_project_desc():
    #BODY 가져오기
    body = json.loads(request.data.decode())
    idx = body["idx"]
    desc = body["desc"]

    result = project.update(idx, "description", desc)
    if result:
        return {"status": 200}
    elif result == 404:
        return {"status": 404}

@app.route("/api/project/update/img/<idx>/", methods=["POST"])
def update_project_img(idx):
    #DB 접속
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("USE logg2;")

    #프로젝트 존재여부
    cursor.execute("select * from project where idx={idx};".format(idx=idx))
    project = cursor.fetchall()

    if len(project) == 0:
        return {"status": 404}
    else:
        code = project[0]["img"]
        if code == None:
            code = random.randint(0, 999999)

        #이미지 저장
        img = request.files["img"]
        img.save(os.path.join(app.config['UPLOAD_FOLDER'], "{}.png".format(code)))

        #DB 내용 변경
        cursor.execute("update project set img={code};".format(code=code))
        conn.commit()
        conn.close()

        return redirect("/project/settings/{idx}/".format(idx=idx))

@app.route("/api/project/get/img/<idx>/", methods=["GET"])
def get_project_img(idx):
    #DB 세팅
    conn = db.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("use logg2;")

    #SELECT
    cursor.execute("select img from project where idx={idx};".format(idx=idx))
    project = cursor.fetchall()

    #404?
    if len(project) == 0:
        return {"status": 404}
    else:
        img = project[0]["img"]
        return send_file("./file/{img}.png".format(img=img), mimetype="image/png")


## 기타 ##
@app.route("/template/")
def template():
    return render_template("template.html")

#debug mode
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3100)
