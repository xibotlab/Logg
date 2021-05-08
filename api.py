import pymysql, json, smtplib
from email.mime.text import MIMEText

#hidden.json 읽기
with open("hidden.json", "r") as f: hidden = json.loads(f.read())

class db():
    @classmethod
    def connect(self):
        return pymysql.connect(host="localhost", user="root", password=hidden["db"]["pw"])
    
    class account():
        def __init__(self):
            self.conn = pymysql.connect(host="localhost", user="root", password=hidden["db"]["pw"])
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            self.cursor.execute("USE logg2")

        def all(self):
            self.cursor.execute("select * from account;")
            return self.cursor.fetchall()

        def email(self, email):
            self.cursor.execute("select * from account where email='{email}';".format(email=email))
            result = self.cursor.fetchall()

            if len(result) == 0:
                return False
            else:
                return result[0]

class account():
    def sendverify(self, email, nickname, code):
        #SMTP 이메일 로그인
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login("xibotlab@gmail.com", hidden["email"]["pw"])

        #인증 메일 전송하기
        msg = MIMEText("""안녕하세요, {nickname}님.
Logg 회원가입 시 필요한 인증코드를 전송해 드립니다.
이 과정을 마치면 {nickname}님은 Logg의 정식 회원으로 등록됩니다.
        
인증코드: {code}
        
Logg에 가입해주셔서 감사합니다.
- Logg 팀 드림""".format(nickname=nickname, code=code))
        msg["subject"] = "[Logg] 인증번호 발송"
        msg['From'] = 'xibotlab@gmail.com'
        msg['To'] = email

        s.send_message(msg)

        s.quit()

        return True

    def signup(self, email, nickname, pw):
        #DB 로그인
        conn = db.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("use logg2;")

        #이미 존재하는 이메일인지 체크
        cursor.execute("SELECT email FROM account WHERE email='{email}';".format(email=email.replace(" ", "")))
        if len(cursor.fetchall()) > 0:
            return "emailerr"

        #insert into db
        cursor.execute('INSERT INTO account (username, password, created, description, email) VALUES ("{nickname}", "{password}", NOW(), "false", "{email}")'.format(nickname=nickname, password=pw, email=email))

        conn.commit()
        conn.close()

        return True

class project():
    def new(self, name, desc, userid):
        #DB 접속
        conn = db.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("USE logg2;")

        #project 테이블에 insert
        cursor.execute("insert into project (name, description) values ('{name}', '{desc}');".format(name=name, desc=desc))

        #생성한 project의 아이디 확인하기
        cursor.execute("select last_insert_id() from project;")
        idx = int(cursor.fetchall()[0]["last_insert_id()"])

        #자동으로 나를 참가하기
        cursor.execute("insert into project_people (userid, projectid, owner) values ({userid}, {projectid}, 1);".format(userid=userid, projectid=idx))

        conn.commit()
        conn.close()

        return 200