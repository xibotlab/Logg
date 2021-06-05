# 소개
Logg는 MoonLab의 프로젝트 관리 서비스입니다.

## 실행
요구사항:
<ul>
 <li>Python</li>
 <li>MySQL</li>
</ul>

pip로 Python 패키지 설치:
```
pip install flask
pip install bcrypt
pip install pymysql
pip install flask_bcrypt
```

MySQL 테이블 설정:
```
create database logg2;
use logg2;
create table account (idx int(11) not null auto_increment, email varchar(50) not null, password varchar(10000) not null, username varchar(50) not null, created datetime not null, description varchar(500) not null, primary key(idx));
create table verify (idx varchar(10) not null, value int(11) not null);
create table project (idx int(11) not null auto_increment, name varchar(50) not null, description varchar(100) not null, public boolean not null default true, img int(11) null, primary key(idx));
create table project_people (idx int(11) not null auto_increment, userid int(11) not null, projectid int(11) not null, owner boolean not null default 0, primary key(idx));
create table tree (idx int(11) not null auto_increment, name varchar(20) not null, projectid int(11) not null, primary key(idx));
```

`hidden.json`을 만들어 다음 내용을 삽입하세요.
```
{
    "db": {
        "pw": MySQL_ROOT_PW
    },
    "email": {
        "pw": EMAIL_APP_PW
    },
    "app": {
        "key": APP_SECRET_KEY
    }
}
```

`app.py`를 실행하고 `localhost:5000`으로 이동하세요. 개발자 모드로 앱을 실행합니다.
