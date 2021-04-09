# Logg
Logg is the social network service from Moonlab.

## Running
Required:
<ul>
 <li>Git</li>
 <li>Python</li>
 <li>MySQL</li>
</ul>

Clone project:
```
git clone https://github.com/xibotlab/logg.git;
```

Installing Python packages:
```
pip install flask
pip install bcrypt
pip install pymysql
```

Set MySQL:
```
create database logg2;
use logg2;
create table account (idx int(11) not null auto_increment, email varchar(50) not null, password varchar(10000) not null, username varchar(50) not null, created datetime not null, description varchar(500) not null, primary key(idx));
```

Create `hidden.json` in cloned directory, than set this information:
```
{
    "db": {
        "pw": database_password
    },
    "email": {
        "pw": your_email_password
    },
    "app": {
        "key": app_secret_key
    }
}
```

Go to `localhost:3000`. Dev mode will open.